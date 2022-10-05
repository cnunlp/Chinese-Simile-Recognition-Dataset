# Chinese-Simile-Recognition-Dataset

## What's new
- 2019/03/02 We have added a Corrigendum section to clarify some typos.  
- 2018/12/10 We have just submitted the *pair-wise evaluate script* used in our paper, and the pretrained word embeddings is also released in /scripts/pretrained_embeddings.emb.

## Contents  
- [Quick Start](#quick-start)
- [Introduction](#introduction)
- [Task Definition](#task-definition)
- [Dataset](#dataset)
  - [Overview](#overview)
  - [Data Format](#data-format)
  - [Labels Definition](#labels-definition)
    - [Labels for Simile Sentence Classification](#labels-for-simile-sentence-classification)
    - [Labels for Simile Component Extraction](#labels-for-simile-component-extraction)
- [Corrigendum](#corrigendum)
- [Reference](#reference)
- [Contact Us](#contact-us)

## Quick Start
This repository contains a chinese simile recognition dataset of "Xiang" which was released with the paper [*Neural Multitask Learning for Simile Recognition*](http://aclweb.org/anthology/D18-1183) by Lizhen Liu, Xiao Hu, Wei Song, Ruiji Fu, Ting Liu, Guoping Hu.

　　**Definition of [*simile*](https://www.merriam-webster.com/dictionary/simile)**: a figure of speech comparing two unlike things that is often introduced by *like* or *as*.

　　**Example**: this boy is as strong as a bull.
  
　　**Task**: given a sentence containing a comparator (*like* in the given example), distinguish whether this sentence is a simile sentence (it is indeed a simile sentence), and extract the tenor (*boy*) and vehicle (*bull*) from it. That is:
  
　　this [boy]<sup>tenor</sup> is as strong as<sup>comparator</sup> a [bull]<sup>vehicle</sup>.
  
　　**Data**: about 11.3k sentences, manually annotated with 1. simile sentence or not, 2. the simile components. The whole dataset was divided into training, development, test set as described in our paper.

## Introduction
A *simile* is a figure of speech that directly compares two things using connecting words such as *like*, *as*, *than* in English and
“像” or “犹如” in Chinese, and these words are called *comparators* (Hanks, 2012) (“喻词”). To some extent, simile is a special type of metaphor, but due to the use of comparators, it is much easier to locate compared with other types of metaphors. As a result, it is possible to collect and annotate large scale of simile sentences and investigate data driven simile recognition. Simile recognition task is to find simile sentences and extract simile components, i.e., the tenor (“本体”) and the vehicle (“喻体”). Here are some example sentences which contains "像", a most frequently used comparator in Chinese.

| Sentence (with translated sentence) | Comment |
| :----------------------- | ------: |
| 这个[孩子]<sup>tenor</sup>壮得**像**一头[牛]<sup>vehicle</sup> | (Metaphorical comparison) |
| 　　This [boy]<sup>tenor</sup> is as strong *as* a [bull]<sup>vehicle</sup> | Simile |
| 这个孩子长得**像**爸爸 | (Literal comparison) |
| 　　The boy looks *like* his father | Literal |
| 他拍拍叔叔的肩膀，**像**是告诉他不要难过 | (As if) |
| 　　He patted his uncle *as if* telling him not to be sad | Literal |
| **像**他这样的学生，应该更加努力 | (To illustrate) |
| 　　The students *like* him should work even harder | Literal |

Notice that a comparator does not always trigger a simile, as shown above, the first two sentences form comparison structures, but the first one triggers a cross-domain concept mapping, while the second one is a literal comparison. The word “像” in the third and fourth sentence means *as if* and *giving examples* respectively, rather than forming a comparison. Simile recognition is still a challenging task because of the diversity of syntactic roles of a word and the distinction between metaphorical and literal comparisons.

This dataset is released in order to support data-driven approaches for simile recognition in Chinese, and the dataset consists of more than 11.3k sentences containing the comparator “像”, in which each sentence was manually annotated with whether it contains a simile, and corresponding simile components.

## Task Definition
*Simile recognition* task is to determine whether a sentence containing a comparator is a simile sentence, if so, extract the tenor and the vehicle from it.

Simile recognition involves two subtasks.

 - **Simile Sentence Classification (SC)**. For a sentence containing a comparator, determine whether the comparator triggers a metaphorical comparison, in another word, whether the sentence is a simile sentence.

 - **Simile Component Extraction (CE)**. For a simile sentence, extract text spans that are corresponding to the tenor and the vehicle objects respectively.

## Dataset
### Overview
This dataset consists of 11.3k sentences extracted from Chinese student essays written in Mandarin Chinese. All sentence in this dataset contains a comparator “像”, and manually annotated with two sets of labels for the two subtasks. Table below shows the basic statistics of our dataset. The whole dataset is divided into three parts, [training set](https://github.com/lingershaw/Chinese-Simile-Recognition-Dataset/blob/master/Chinese-Simile-Recognition-Dataset-Train.csv), [development set](https://github.com/lingershaw/Chinese-Simile-Recognition-Dataset/blob/master/Chinese-Simile-Recognition-Dataset-Dev.csv), and [test set](https://github.com/lingershaw/Chinese-Simile-Recognition-Dataset/blob/master/Chinese-Simile-Recognition-Dataset-Test.csv), and the proportion is about 0.64:0.16:0.20. All results in our paper is obtained in this test set.

| Item | Number |
| :----------------------- | :------: |
|\#All Sentence | 11337  |
|\#Simile Sentence | 5088  |
|\#Literal Sentence | 6249 |
|\#Tokens | 334k |
|\#Tenor | 5183 |
|\#Vehicle | 5119 |
|\#Unique tenor concept | 1680 |
|\#Unique vehicle concept | 1972 |
|\#Tenor-vehicle pair | 5214 |
|\#Unique tenor-vehicle pair | 4521 |
|Avg. \#tokens per tenor | 1.033 |
|Avg. \#tokens per vehicle | 1.056 |
|Avg. \#tokens per sentence | 29.47 |
|Avg. \#pair per simile sentence | 1.024 |

### Data Format
The sentences are basically in CoNLL-type tab-separated format. With classification label in the first line, and one word per line in the following lines, separate column for token and label for component extraction, empty line between sentences. Here is an example:

    simile
    那	O
    雨	ts
    咆哮	O
    着	O
    ，	O
    肆无忌惮	O
    地下	O
    着	O
    ，	O
    像	O
    恶魔	vs
    。 O
    

which means:

    (Classification label indicating whether this sentence is a simile sentence)
    (token 1)   (component extraction label for token 1)
    (token 2)   (component extraction label for token 2)
    (token 3)   (component extraction label for token 3)
    ...
    (token n)   (component extraction label for token n)
    

### Labels Definition
#### Labels for Simile Sentence Classification
Labels for simile sentence classification are assigned to each sentence.

| Label | Meaning |
| :----------------------- | :------ |
| Simile | This sentence contains a simile. |
| Literal | This sentence does not contain any simile.|

#### Labels for Simile Component Extraction
Different from labels for simile sentence classification, labels for simile component extraction are in token level. We focus on the two kinds of main simile components, t(enor) and v(ehicle). We convert the annotation to IOBES scheme (indicating Inside, Outside, Beginning, Ending, Single) (Ratinov and Roth, 2009), so there are 9 labels in total, as shown in the table:

| Label | Meaning |
| :----------------------- | :------ |
| ts | A single word tenor |
| tb | The begining of a tenor |
| tm | The middle of a tenor |
| te | The end of a tenor |
| vs | A single word vehicle |
| vb | The begining of a vehicle |
| vm | The middle of a vehicle |
| ve | The end of a vehicle |
| O | None |

## Corrigendum
1. page 1546 -> 4.2 Shared Representation -> formula (1)   
  Original:  
　　<a href="https://www.codecogs.com/eqnedit.php?latex=\overrightarrow{h_t}=LSTM(x_{t},&space;LSTM(\overrightarrow{h_{t-1}}))" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\overrightarrow{h_t}=LSTM(x_{t},&space;LSTM(\overrightarrow{h_{t-1}}))" title="\overrightarrow{h_t}=LSTM(x_{t}, LSTM(\overrightarrow{h_{t-1}}))" /></a>  
  Revised:  
　　<a href="https://www.codecogs.com/eqnedit.php?latex=\overrightarrow{h_t}=LSTM(x_{t},&space;\overrightarrow{h_{t-1}})" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\overrightarrow{h_t}=LSTM(x_{t},&space;\overrightarrow{h_{t-1}})" title="\overrightarrow{h_t}=LSTM(x_{t}, \overrightarrow{h_{t-1}})" /></a>  
2. page 1548 -> 4.5 Task 3: Language Modeling -> paragragh 3 -> line 1  
  Original:  
　　And the ***vehicle*** word is predicted by maximizing  
  Revised:  
　　And the ***target*** word is predicted by maximizing  

## Reference
The dataset is released with this paper:
```bibtex
    @InProceedings{D18-1183,
      author = 	"Liu, Lizhen
            and Hu, Xiao
            and Song, Wei
            and Fu, Ruiji
            and Liu, Ting
            and Hu, Guoping",
      title = 	"Neural Multitask Learning for Simile Recognition",
      booktitle = 	"Proceedings of the 2018 Conference on Empirical Methods in Natural Language Processing",
      year = 	"2018",
      publisher = 	"Association for Computational Linguistics",
      pages = 	"1543--1553",
      location = 	"Brussels, Belgium",
      url = 	"http://aclweb.org/anthology/D18-1183"
    }
```
The references of explaining simile concepts and some other references:

[1] Patrick Hanks. 2012. The roles and structure of comparisons, similes, and metaphors in natural language (an analogical system). Prose (in honor of the Dickens Bicentennial), page 5.

[2] Lev Ratinov and Dan Roth. 2009. Conll ’09 design challenges and misconceptions in named entity recognition. In CoNLL ’09: Proceedings of
the Thirteenth Conference on Computational Natural Language Learning, pages 147–155.

## Contact Us
If you have any questions, feel free to contact Hu, Xiao at xiaohu@cnu.edu.cn, I will offer some help with all my efforts.
