# coding=utf-8
# Pairwise evaluation script for repo Chinese-Simile-Recognition-Dataset.
# We adopted grouped (t)enor and (v)ehicle chunks in a sentence as t-v pairs, and evaluate the difference between 
#  gold annotations and predicted results based on the count of t-v pairs.
# The input of this script should be an iterable object, just modify the iterable2sents function to fit your own 
#  format and generate list of sentences containg tokens, labels_true, labels_pred. By default, a conll format file 
#  is recommanded, an example is given in the predicted_example.tsv. The output of 
#  "python paireval.py predicted_example.tsv" should be 
#  "processed 104 tokens with 2 pairs; found: 3 pairs; correct: 1. precision:  33.33%; recall:  50.00%; FB1:  40.00".
# Modified from conll evaluation script, https://github.com/marekrei/sequence-labeler/blob/master/conlleval.py

import sys
from collections import defaultdict


class FormatError(Exception):
    pass


def end_of_chunk(prev_tag, tag, prev_type, type_):
    # check if a chunk ended between the previous and current word
    # arguments: previous and current chunk tags, previous and current types
    chunk_end = False
    if prev_tag == 'e'or prev_tag == 's': chunk_end = True
    if prev_tag == 'b' and tag == 'b': chunk_end = True
    if prev_tag == 'b' and tag == 's': chunk_end = True
    if prev_tag == 'b' and tag == 'O': chunk_end = True
    if prev_tag == 'm' and tag == 'b': chunk_end = True
    if prev_tag == 'm' and tag == 's': chunk_end = True
    if prev_tag == 'm' and tag == 'O': chunk_end = True
    if prev_tag != 'O' and prev_type != type_: chunk_end = True
    return chunk_end


def start_of_chunk(prev_tag, tag, prev_type, type_):
    # check if a chunk started between the previous and current word
    # arguments: previous and current chunk tags, previous and current types
    chunk_start = False
    if tag == 'b' or tag == 's': chunk_start = True
    if prev_tag == 'e' and tag == 'e': chunk_start = True
    if prev_tag == 'e' and tag == 'm': chunk_start = True
    if prev_tag == 's' and tag == 'e': chunk_start = True
    if prev_tag == 's' and tag == 'm': chunk_start = True
    if prev_tag == 'O' and tag == 'e': chunk_start = True
    if prev_tag == 'O' and tag == 'm': chunk_start = True
    if tag != 'O' and prev_type != type_: chunk_start = True
    return chunk_start


def parse_tag(t):
    if t == 'O':
        return ('O', 'O')
    if len(t) == 2:
        return t[0], t[1]
    else:
        raise FormatError('unexpected tags when pasing: ', t)


def detect_chunks(labels_predicted, labels_true):
    # calculate correct chunks of labels_predicted
    t_correct_chunk = defaultdict(int)
    in_correct = False        # currently processed chunks is correct until now
    last_correct = 'O'        # previous chunk tag in corpus
    last_correct_type = ''    # type of previously identified chunk tag
    last_guessed = 'O'        # previously identified chunk tag
    last_guessed_type = ''

    for i in range(len(labels_predicted)):
        label_predicted = labels_predicted[i]
        label_true = labels_true[i]

        guessed_type, guessed = parse_tag(label_predicted)
        correct_type, correct = parse_tag(label_true)
        end_correct = end_of_chunk(last_correct, correct, last_correct_type, correct_type)
        end_guessed = end_of_chunk(last_guessed, guessed, last_guessed_type, guessed_type)
        start_correct = start_of_chunk(last_correct, correct, last_correct_type, correct_type)
        start_guessed = start_of_chunk(last_guessed, guessed, last_guessed_type, guessed_type)

        if in_correct:
            if (end_correct and end_guessed and last_guessed_type == last_correct_type):
                in_correct = False
                t_correct_chunk[last_correct_type] += 1
            elif (end_correct != end_guessed or guessed_type != correct_type):
                in_correct = False

        if start_correct and start_guessed and guessed_type == correct_type:
            in_correct = True

        last_guessed = guessed
        last_correct = correct
        last_guessed_type = guessed_type
        last_correct_type = correct_type
    if in_correct:
        t_correct_chunk[last_correct_type] += 1
    return(t_correct_chunk)


def count_t_and_v(labels):
    num_t, num_v = 0, 0
    last_label = 'O'        # previously identified chunk tag
    last_label_type = ''
    for i in labels:
        label_type, label = parse_tag(i)
        if start_of_chunk(last_label, label, last_label_type, label_type):
            if label_type == 'v': num_v += 1
            if label_type == 't': num_t += 1
        last_label = label
        last_label_type = label_type
    return num_t, num_v


def iterable2sents(iterable):
    sents = []
    tokens, labels_true, labels_pred = [], [], []
    for line in iterable:
        if line.strip() == '':
            sents.append([tokens, labels_true, labels_pred])
            tokens, labels_true, labels_pred = [], [], []
            continue
        line_parts = line.strip().split('\t')
        tokens.append(line_parts[0])
        labels_true.append(line_parts[1])
        labels_pred.append(line_parts[2])
    return sents


def evaluate(iterable, report=False):
    # For gold labels, the count of tenor and vehicle could be 0-0, 1-1, 1-many, many-1, so the max number of tenor and vehicle is the true tenor-vehicle pairs.
    # For predicted labels, we simplify the total number of predicted tenor-vehicle pairs to the max number of tenor and vehicle, too.
    sents = iterable2sents(iterable)

    token_counter = 0
    true_pair, pred_pair, pair_hit = 0, 0, 0
    for i in range(len(sents)):
        token_counter += len(sents[i][0])
        _, labels_true, labels_pred = sents[i]
        num_t, num_v = count_t_and_v(labels_true)
        num_t_pred, num_v_pred = count_t_and_v(labels_pred)
        true_pair += max(num_t, num_v)
        pred_pair += max(num_t_pred, num_v_pred)
        correct_chunk = detect_chunks(labels_pred, labels_true)
        if num_t == 1 and num_v == 1:
            if correct_chunk['t'] == 1 and correct_chunk['v'] == 1:
                pair_hit += 1
        elif num_t > 1 and num_v > 1:
            if correct_chunk['t']==0 or correct_chunk['v']==0:
                pair_hit+=0
            else:
                pair_hit+=max(correct_chunk['v'], correct_chunk['t'])
        elif num_t > 1 and num_v == 1:
            pair_hit += correct_chunk['t'] if correct_chunk['v'] == 1 else 0
        elif num_t == 1 and num_v > 1:
            pair_hit += correct_chunk['v'] if correct_chunk['t'] == 1 else 0
        elif num_t == 0 and num_v == 0:
            pass
        else:
            assert(False)

    recall = 0.0 if true_pair == 0 else (1.0 * pair_hit / true_pair)
    precision = 0.0 if pred_pair == 0 else (1.0 * pair_hit / pred_pair)
    f_1 = 0.0 if (precision + recall) == 0.0 else 2 * precision * recall / (precision + recall)

    if report:
        out = sys.stdout
        out.write('processed %d tokens with %d pairs; ' %
                  (token_counter, true_pair))
        out.write('found: %d pairs; correct: %d.\n' %
                  (pred_pair, pair_hit))
        if token_counter > 0:
            out.write('precision: %6.2f%%; ' % (100. * precision))
            out.write('recall: %6.2f%%; ' % (100. * recall))
            out.write('FB1: %6.2f\n' % (100. * f_1))

    return token_counter, precision, recall, f_1


if __name__ == '__main__':
    with open(sys.argv[1], 'r', encoding='utf-8') as f:
        evaluate(f, report=True)
