# Chinese-Simile-Recognition-Dataset

## Quick Start
This repository contains a chinese simile recognition dataset of "Xiang" which was released with the paper [*Neural Multitask Learning for Simile Recognition*](http://aclweb.org/anthology/D18-1183) by Lizhen Liu, Xiao Hu, Wei Song, Ruiji Fu, Ting Liu, Guoping Hu.

　　Definition of [*simile*](https://www.merriam-webster.com/dictionary/simile): A figure of speech comparing two unlike things that is often introduced by like or as.

　　Example: This [boy]<sup>tenor</sup> is as strong as<sup>comparator</sup> a [bull]<sup>vehicle</sup>.

## Introduction
A *simile* is a figure of speech that directly compares two things using connecting words such as *like*, *as*, *than* in English and
“像” or “犹如” in Chinese, and these words are called *comparators* (“喻词”). To some extent, simile is a special type of metaphor, but compared with other types of metaphors, it is much easier to locate due to the use of comparators. As a result, it is possible to collect and annotate large scale of simile sentences and investigate data driven simile recognition. This task is to find simile sentences and extract simile components, i.e., the tenor (“本体”) and the vehicle (“喻体”). Here are some example sentences which contains "像", a most frequently used comparator in Chinese.

| Sentence (with translated sentence) | Comment |
| :----------------------- | ------: |
| 这个[孩子]<sup>tenor</sup>壮得**像**一头[牛]<sup>vehicle</sup> | (Metaphorical comparison) |
| 　　This [boy]<sup>tenor</sup> is as strong as a [bull]<sup>vehicle</sup> | Simile |
| 这个孩子长得**像**爸爸 | (Literal comparison) |
| 　　The boy looks like his father | Literal |
| 他拍拍叔叔的肩膀，**像**是告诉他不要难过 | (As if) |
| 　　He patted his uncle as if telling him not to be sad | Literal |
| **像**他这样的学生，应该更加努力 | (To illustrate) |
| 　　The students like him should work even harder | Literal |

Notice that a comparator does not always trigger a simile, as shown above, the first two sentences form comparison structures, but the first one triggers a cross-domain concept mapping, while the second one is a literal comparison. The word “像” in the third and fourth sentence means *as if* and *giving examples* respectively, rather than forming a comparison.

Simile recognition is still a challenge task because of the diversity of syntactic roles of a word and the distinction between metaphorical and literal comparisons. This dataset is released in order to support data-driven approaches for simile recognition in Chinese, and the dataset consists of 11.3k sentences containing the comparator “像”, in which each sentence are manually annotated with whether it contains a simile, and corresponding simile components.

## Task Definition
*Simile recognition* task is to determine whether a sentence containing a comparator is a simile sentence, if so, extract the tenor and the vehicle from it.

Simile recognition involves two subtasks.

Simile Sentence Classification (SC). For a sentence containing a comparator, determine whether the comparator triggers a metaphorical comparison, in another word, whether the sentence is a simile sentence.

Simile Component Extraction (CE). For a simile sentence, extract text spans that are corresponding to the tenor and the vehicle objects respectively.

## Dataset
### Overview
This dataset consists of 11.3k sentences extracted from Chinese student essays written in Mandarin Chinese. All sentence in this dataset contains a comparator “像”, and manually annotated with two sets of labels for the two subtasks. The whole dataset is divided into three parts, [training set](https://github.com/lingershaw/Chinese-Simile-Recognition-Dataset/blob/master/Chinese-Simile-Recognition-Dataset-Train.csv), [development set](https://github.com/lingershaw/Chinese-Simile-Recognition-Dataset/blob/master/Chinese-Simile-Recognition-Dataset-Dev.csv), and [test set](https://github.com/lingershaw/Chinese-Simile-Recognition-Dataset/blob/master/Chinese-Simile-Recognition-Dataset-Test.csv), and the proportion is about 0.64:0.16:0.20. All results in our paper is obtained in this test set. Table below shows the basic statistics of our dataset.

| Item | Number |
| :----------------------- | :------: |
|\#All Sentence | 11337  |
|\#Simile Sentence | 5088  |
|\#Literal Sentence | 6249 |
|\#Tokens | 334*k* |
|\#Tenor | 5183 |
|\#Vehicle | 5119 |
|\#Tenor-vehicle Pairs | 5214 |
|Avg. \#Tokens per Tenor | 1 |
|Avg. \#Tokens per Vehicle | 1.056 |
|Avg. \#Tokens per Sentence | 29 |
|Avg. \#Pair per Simile Sentence | 1.024 |
|\#Tenor concepts | 1680 |
|\#Vehicle concepts | 1972 |
|\#Unique Tenor-vehicle Pairs | 4521 |

## Data Format
The data is basically in CoNLL-type tab-separated format. Classification label in the first line, and one word per line in the following lines, separate column for token and label for component extraction, empty line between sentences. Here is an example:

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
    (token 1) (component extraction label for token 1)
    (token 2) (component extraction label for token 2)
    (token 3) (component extraction label for token 3)
    ...
    (token n) (component extraction label for token n)

## Meaning of labels
#### Classification labels
Classification labels are in sentence level, and is assigned to each sentence.
| Label | Meaning |
| :----------------------- | ------: |
| Simile | This sentence contains a simile. |
| Literal | This sentence does not contain any simile.|
#### Component extraction labels
Different from classification labels, component extraction labels are in token level. We forcus on the two kinds of main simile component, t(enor) and v(ehicle). We convert the annotation to IOBES scheme (indicating Inside, Outside, Beginning, Ending, Single) (Ratinov and Roth , 2009), so there are 9 labels in total, as shown in the table:

| Label | Meaning |
| :----------------------- | :------ |
| ts | A single word tenor |
| tb | The begining of tenor |
| tm | The middle of tenor |
| te | The end of tenor |
| vs | A single word vehicle |
| vb | The begining of vehicle |
| vm | The middle of vehicle |
| ve | The end of vehicle |
| O | Not component |

## Reference
Patrick Hanks. 2012. The roles and structure of comparisons, similes, and metaphors in natural language (an analogical system). Prose (in honor of the Dickens Bicentennial), page 5.
Lev Ratinov and Dan Roth. 2009. Conll ’09 design challenges and misconceptions in named entity recognition. In CoNLL ’09: Proceedings of
the Thirteenth Conference on Computational Natural Language Learning, pages 147–155.
