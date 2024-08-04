# minGPT
项目内容主要包括基于minGPT架构的GPT模型构建、预训练、微调、优化的全流程。

## GPT模型构建

minGPT是GPT原始模型的简洁版本，具有更小的参数数量和更透明的某些架构。

这里我们构建的模型基于minGPT,核心Block层数为4，多头head数量为8。

最后，我们除了基础的GPT模型还同时考虑了GPT变种：Perceiver GPT的性能表现。

该GPT变种结构与GPT基础模型大致相似，只是中间BLOCK输出向量维度变小了（输入、输出层维度不变）。

Perceiver GPT是为了追求efficiency而产生的。

## GPT模型预训练

我们选择的预训练处理是：span corruption。其针对一个语句，处理方式如下：（目标任务仍然是language modeling）

```
0. 使用 __getitem__ 的 idx 参数检索 self.data 中位于给定索引处的元素。我们将把得到的数据条目称为文档。
1. 随机截断文档，使其长度不小于 4 个字符、且不超过 int(self.block_size*7/8) 个字符。
2. 现在，把（截断的）文档分成三个子串：
[前缀] [屏蔽内容] [后缀］
屏蔽内容的长度应该是随机的，平均为截断文档长度的 1/4。
3. 将这些子串重新排列成以下形式：
[前缀] MASK_CHAR [后缀] MASK_CHAR [屏蔽内容] [pad］
生成的字符串称为 masked_string，作为输出示例。这里的 MASK_CHAR 是《词汇规范》中定义的屏蔽字符。[pads] 是一串重复的 PAD_CHAR 字符，因此整个字符串的长度为self.block_size。这样处理后，[masked_content]会从文件中移除，并用MASK_CHAR 字符替换。（定义的屏蔽字符）。
4. 现在，我们使用 masked_string 来构建输入和输出示例对。为此输入字符串为 masked_string[:-1]，输出字符串为 masked_string[:-1]。换句话说，对于每个字符，我们的目标是预测屏蔽字符串中的下一个字符。
5.利用定义的词汇表，将结果输入和输出字符串编码张量，并返回。
```

预训练文本和之后的微调目标任务相似，来自于Wikipedia，包含了不同名人的身份介绍，包含了其出生地点、身份、事迹等。

## 模型微调

模型微调的目标任务是名人出生地点问答题：

Train set:

```
Where was Khatchig Mouradian born?	Lebanon
Where was Jacob Henry Studer born?	Columbus
Where was John Stephen born?	Glasgow
Where was Georgina Willis born?	Australia
......
```

Testset:

```
Where was Adam Bright born?
Where was Alan Hess born?
Where was Jacob Guptil Fletcher born?
Where was Hisham Mohd Ashour born?
......
```

微调的训练时，仍然是language modeling。预测时，则是采样。

## 模型优化

为了提升模型efficienccy，采用了Perciever GPT变种。

该方法的核心在于，针对GPT的中间Block,不一定需要输入或是输出时那么大的维度数。因此，针对第一个BLOCK的输出会有一个降秩矩阵，降低维度数；针对倒数第二个BLOCK的输出会有升秩矩阵，还原维度为要求维度数。

