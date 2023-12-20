# SOLUTION SKETCH

## Search Technology Mock Exam 2023 solution sketch

## True / False, and justify your answer

### Q1: The _Kendall tau coefficient_ is a measure of the correspondence between two rankings. A value of 0 indicates perfect disagreement between the rankings.

A1: False. A value of 0 indicates either a random relationship or none at all between the rankings, since the lowest is -1 and the highest is 1.

### Q2: As _Support Vector Machines_ are inherently binary classifiers, they are not useful for multi-classification.

A2: Depends. While a single SVM cannot classify multiple classes alone, it can be combined with other SVMs. E.g., for the classes A, B and C, we have the following options: Train SVMs for A vs. not A, B vs. not B, and C vs. not C. We can also train them for A vs B, B vs C, and A vs C. There _are_ also multi-class SVM algorithms designed to handle multiple classes directly, such as Crammer-Singer SVM, but that is not within the scope of our curriculum.

## Mixed grill

### Q3: What is the _suffix array_ for the string “informatics”?

A3: [6, 9, 2, 8, 0, 5, 1, 3, 4, 10, 7]. [('atics', 6), ('cs', 9), ('formatics', 2), ('ics', 8), ('informatics', 0), ('matics', 5), ('nformatics', 1), ('ormatics', 3), ('rmatics', 4), ('s', 10), ('tics', 7)]

### Q4: Describe the formula for _Heap’s law_, and its use case.

A4: Heap's law: M=k×T^β, where M is the vocabulary size, T is the number of tokens. k and β are empirical constants. It is used to model vocabulary growth concerning the size of the document collection.

### Q5: _MapReduce_ is a model of distributed processing. What happens during the Map phase, and what happens during the Reduce phase?

A5: In the Map phase of MapReduce, data is divided into chunks and processed in parallel, producing key-value pairs. The Reduce phase aggregates and combines these key-value pairs based on their keys.

### Q6: Explain _Precision@k_ and _MAP_, and how one depends on the other.

A6: Precision@k measures the precision of the top k retrieved documents. Mean Average Precision (MAP) calculates the average of precision scores for different query results. Precision@k is a component of MAP; improving Precision@k contributes to an increased MAP score.

## Discuss: Precision & Recall

### Q7: In the context of search engines, discuss practical scenarios where _high precision_ but _low recall_ might be preferred, and vice versa.

A7: Scenarios where we prefer high recall:

1. Search and Rescue Operations: In emergencies, you'd want to ensure you don't miss any relevant information, locations, or people in distress. High recall ensures that all potential leads are considered.
2. Medical Screening: In medical screenings, it's crucial not to miss any potential health risks. High recall helps in ensuring that no critical conditions are overlooked, even if some false alarms are raised.
3. Informational Research: During the exploration phase of a research project, having access to as much relevant information as possible is essential, even if some irrelevant data is included.
4. Customer Service Complaints: Ensuring all customer complaints and issues are addressed is vital for maintaining customer satisfaction and addressing service concerns.
5. Fraud Detection: Financial institutions and cybersecurity systems prefer high recall to catch all potential fraudulent activities, even if it means going through some false positives.

Scenarios where we prefer high precision:

1. Cancer Diagnosis: In cancer diagnoses, high precision is essential to avoid misdiagnoses and ensure the accuracy of the information provided to patients.
2. Legal Documents: In legal cases, precision is vital to provide accurate and relevant references, case laws, and statutes, ensuring only the most relevant information is presented.
3. Recommendation Systems: For personalized recommendations in e-commerce or content platforms, high precision ensures that the user is presented with accurate suggestions, avoiding irrelevant items.
4. Air Traffic Control: Precision is key in air traffic control systems to ensure that only accurate and verified information is used for decision-making, avoiding unnecessary alarms.
5. News Aggregation: Precision is essential to prevent the spread of misinformation. Validating and ensuring the accuracy of news articles before dissemination is vital in this context.
