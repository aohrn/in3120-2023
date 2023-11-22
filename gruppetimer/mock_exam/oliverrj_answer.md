# Live solution

2023-11-21 10:15 @ Prolog
oliverrj, TA
This is my live solution written during the mock exam.

## True / False, and justify your answer

### Q1: The _Kendall tau coefficient_ is a measure of the correspondence between two rankings. A value of 0 indicates perfect disagreement between the rankings.

The 'Kendall-tau coefficient', most often referred to as Kendall Tau distance is a measure of the equality of the order of to lists. In the context of our course we typically use this as a metric for comparison of various ranking methods, i.e. measure how similar/different various ranking approaches are. The value provided by calculating Kendall tau distance is the same as the number of swaps in a bubble sort-algorithm for sorting one of the lists to equal the other. Because of this, the value 0 indicates that the lists are identical and the statement is therefore false.

**This answer is wrong - kendall tau distance and kendall tau coefficient are not the same thing. The answer is true for kendall tau distance (which is also a part of the curriculum)**

### Q2: As _Support Vector Machines_ are inherently binary classifiers, they are not useful for multi-classification.

False, they are useful. While it is true that a _single_ SVM can not be applied for this, we can achieve multi class classification by using several SVMs.

## Mixed grill

### Q4: What is the _suffix array_ for the string “informatics”?

The suffix array of a token is a list of all the indeces of the characters, sorted in such a way that the substrings are in alphabetical order.

The indeces are, in sorted order: [6, 9, 2, 8, 0, 5, 1, 3, 4, 10, 7].

This corresponds to the following suffixes:
[
('atics', 6),
('cs', 9),
('formatics', 2),
('ics', 8), ('informatics', 0),
('matics', 5),
('nformatics', 1),
('ormatics', 3),
('rmatics', 4),
('s', 10),
('tics', 7)
]

^ Note how the strings are in alphabetical order.

### Q5: Describe the formula for _Heap’s law_, and its use case.

Heap's law is a formula that allows us to calculate an estimate for the number of types of a given collection. I.e. , it answers "_if we have this many tokens, how many of them will be unique?_". The formula is M=kxT^B where T is the number of tokens and k and B are empircal constants.
Typically k and B are between 10,100 and 0.4, 0.6 for english. These numbers have been found to be the best upon emperical inspection.

Keyword: type-token relation.

### Q6: _MapReduce_ is a model of distributed processing. What happens during the Map phase, and what happens during the Reduce phase?

MapReduce archiechture consists of having several jobs running. Some of the jobs are mappers, and some of the jobs are reducers. The mappers each get a chunk of the data that is to be processed and they process these. After data processing, the reducers take the result from the processsing and yield results.

What specifically happens will depend on the specific MapReduce-job, i.e. what kind of data is being processed and what kind of algorithm is being applied to it.

### Q7: Explain _Precision@k_ and _MAP_, and how one depends on the other.

Precision@k and MAP(mean average precision) are boths metrics for information retrieval system evaluation.

Precision@k yields the precision of the k best (i.e. most highly ranked) matches for a query given a value k. I.e. , of the k best elements in the ranking set, how many of them were TP (true positive, actually relevant, supposed to be there etc. )

mAP, as the name might imply, yields an average over sevaral values k for precision@k. I.e. mAP provides a smoothed estimate for precision@k without being overly reliant on any single value k.

Increasing precision@k will increase mAP, and indicte your search system achieving overall better IR results as the amount of TP will have increased.

## Discuss: Precision & Recall

### Q8: In the context of search engines, discuss practical scenarios where _high precision_ but _low recall_ might be preferred, and vice versa.

Precision indicates our confidence in declaring something to be relevant, i.e. with 100% precision we would never have a FP(false positive).
Recall indicates our ability to find all relevant matches (i.e. there are no TN(true negatives) we don't retrieve)\*.

\*a way of achieving 100% perfect recall is to say that _all documents_ in your systems are relevant, but this is impractical as we cannot rank all these items.

Generally we want high precision if having a FP(false positive) can have negative resulst. E.g. if a docter diagnoses a patient with having some bad condition, it would not be good to have the doctor have low precision, i.e. having FP, i.e. saying to a perfectly healthy person that they might be in for a bad time.

Recall is important in the cases where leaving something out can be detrimental. E.g. if you are a lawyer trying to win a case and you search for some very specific law that could ensure your victory, but you're unable to find it due to the system having low recall such that you lose your case.
