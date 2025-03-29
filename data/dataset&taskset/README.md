<br>

# Datasets Table

| Dataset Name       | Dataset Theme                     | Dataset Source                                | Sample Size | Number of Features | Data Types                    |
|--------------------|-----------------------------------|-----------------------------------------------|-------------|--------------------|-------------------------------|
| Adult.csv | Socioeconomic | UCI Machine Learning Repository | 32,561 | 15 | Categorical, Numerical |
| COMPAS.csv          | Crime         | ProPublica | 60,843 | 28                 | Categorical, Numerical   |
| Statlog(German Credit).csv             | Financial | UCI Machine Learning Repository | 1,000   | 21                 | Categorical, Numerical    |
| MIMIC-IV.csv        | Healthcare | Medical Information Mart for Intensive Care  | 1,081 | 10                 | Categorical, Numerical   |
| Student Performance.csv            | Education | UCI Machine Learning Repository | 395   | 33                 | Categorical, Numerical   |

<br><br>

# Datasets Overview and Feature Descriptions

## Adult.csv

### Dataset Overview
The **Adult Dataset** (also known as the "Census Income" dataset) is a widely used dataset from the **UCI Machine Learning Repository**. It contains demographic information about individuals, including age, work class, education, marital status, occupation, race, and sex. The primary objective of this dataset is to predict whether an individual earns more than $50K per year based on their attributes. It is frequently used in machine learning tasks related to classification, bias detection, and fairness in predictions, especially concerning income disparities across different demographic groups such as gender and race.

### Citation
Becker, B., & Kohavi, R. (1996). Adult [Dataset]. UCI Machine Learning Repository. [https://doi.org/10.24432/C5XW20](https://doi.org/10.24432/C5XW20)

### Feature Descriptions and Definitions

1. **age (Age)**  
   The age of the individual. This feature is crucial for analyzing age-related income trends and disparities in economic opportunities.

2. **workclass (Work Class)**  
   Describes the individual’s employment status, such as private sector, self-employed, government, or never worked. It helps in assessing employment patterns and their influence on income levels.

3. **fnlwgt (Final Weight)**  
   A calculated weight representing the number of people the individual represents in the U.S. population. This feature is useful in census data to balance the dataset and make inferences about population-level trends.

4. **education (Education Level)**  
   The highest level of education attained by the individual, such as high school, bachelor’s degree, or master’s degree. This feature plays a significant role in understanding how education impacts earning potential.

5. **education-num (Years of Education)**  
   A numeric representation of the individual’s education level. It is closely related to the "education" feature and is used for analysis involving numeric computations.

6. **marital-status (Marital Status)**  
   Indicates the individual's marital status, such as married, never married, or divorced. Marital status can influence income levels, social support, and economic stability.

7. **occupation (Occupation)**  
   The occupation of the individual, such as tech support, sales, or executive management. It is a key factor in determining income, as certain occupations tend to have higher earning potential.

8. **relationship (Relationship)**  
   Describes the individual's family relationship within a household, such as husband, wife, or not-in-family. This feature helps in understanding the role of family structure in income dynamics.

9. **race (Race)**  
   The individual’s race, which includes categories such as White, Black, Asian-Pac-Islander, and others. This feature is essential for studying racial disparities in income and employment opportunities.

10. **sex (Gender)**  
    The gender of the individual, typically recorded as male or female. Gender is a critical feature for analyzing gender pay gaps and employment inequality.

11. **capital-gain (Capital Gain)**  
    The income earned from capital gains investments. This feature is relevant for understanding the impact of investment income on overall earnings.

12. **capital-loss (Capital Loss)**  
    The losses from capital investments. It helps in analyzing the economic behaviors of individuals who engage in investment activities.

13. **hours-per-week (Hours Worked Per Week)**  
    The number of hours the individual works per week. This feature is important for understanding labor contributions and its relationship to income.

14. **native-country (Native Country)**  
    The individual's country of origin. This feature can provide insights into how country of origin influences economic opportunities and outcomes.

15. **income (Income Class)**  
    The target variable that indicates whether an individual's income exceeds $50K per year, classified as either ">50K" or "<=50K". This is the main variable used in predictive modeling tasks related to income classification and fairness analysis.

<br><br>

## COMPAS.csv

### Dataset Overview
The **COMPAS (Correctional Offender Management Profiling for Alternative Sanctions)** dataset contains information used in the criminal justice system to predict recidivism risk. It was collected as part of a study on algorithmic bias by **ProPublica**. The dataset includes demographic information (such as name, gender, and race), criminal history, risk assessment scores, and other details generated by the COMPAS algorithm. It is widely used to examine bias in algorithmic decision-making, particularly regarding racial disparities in recidivism predictions.

### Citation
Larson, J., Mattu, S., Kirchner, L., & Angwin, J. (2016). *COMPAS analysis*. GitHub. Available at: [https://github.com/propublica/compas-analysis](https://github.com/propublica/compas-analysis).

### Feature Descriptions and Definitions

1. **Person_ID**  
   A unique identifier for each defendant.

2. **AssessmentID**  
   A unique identifier for each assessment, linking to different assessment records.

3. **Case_ID**  
   A unique identifier for the defendant in a specific case.

4. **Agency_Text**  
   The name of the agency conducting the assessment.

5. **LastName**  
   The defendant’s last name.

6. **FirstName**  
   The defendant’s first name.

7. **MiddleName**  
   The defendant’s middle name, or NULL if none.

8. **Sex_Code_Text**  
   The defendant’s gender, typically recorded as male or female.

9. **Ethnic_Code_Text**  
   The defendant’s race, e.g., "Caucasian."

10. **DateOfBirth**  
    The defendant’s date of birth.

11. **ScaleSet_ID**  
    An identifier for the scaleset used in the risk assessment.

12. **ScaleSet**  
    The type of scaleset used in the assessment

13. **AssessmentReason**  
    The reason for the assessment

14. **Language**  
    The primary language spoken by the defendant.

15. **LegalStatus**  
    The current legal status of the defendant

16. **CustodyStatus**  
    The custody status of the defendant

17. **MaritalStatus**  
    The defendant’s marital status

18. **Screening_Date**  
    The date the COMPAS screening was conducted.

19. **RecSupervisionLevel**  
    The supervision level recommended by COMPAS, typically a numeric level.

20. **RecSupervisionLevelText**  
    The textual description of the recommended supervision level

21. **Scale_ID**  
    The identifier of the specific scale associated with the assessment.

22. **DisplayText**  
    The description text of the scale

23. **RawScore**  
    The raw score generated by the assessment, often a negative number representing the computed result of the algorithm.

24. **DecileScore**  
    A risk score ranging from 1 to 10, with higher scores indicating higher risk.

25. **ScoreText**  
    A textual description of the score

26. **AssessmentType**  
    The type of assessment

27. **IsCompleted**  
    A binary indicator showing whether the assessment was completed.

28. **IsDeleted**  
    A binary indicator showing whether the assessment was deleted.

<br><br>

## Statlog (German Credit Data).csv

### Dataset Overview
The **Statlog (German Credit Data)** dataset is a well-known dataset from the **UCI Machine Learning Repository**. It contains information about individuals and their credit history, with the goal of classifying individuals into good or bad credit risk categories. The dataset includes a variety of financial and demographic features such as the duration of the loan, credit amount, and the individual's personal information. This dataset is widely used in machine learning tasks related to credit risk classification and has been a benchmark in various studies on algorithmic bias and fairness in financial decision-making.

### Citation
Hofmann, H. (1994). Statlog (German Credit Data) [Dataset]. UCI Machine Learning Repository. [https://doi.org/10.24432/C5NC77](https://doi.org/10.24432/C5NC77).

### Feature Descriptions and Definitions

1. **Status of existing checking account**  
   Describes the status of the individual’s checking account, categorized into different risk levels based on balance and overdraft.

2. **Duration in months**  
   The duration of the loan or credit in months. This feature helps in understanding the repayment timeline.

3. **Credit history**  
   Records the individual’s credit history, including previous loans and any past defaults, providing context on the borrower’s risk level.

4. **Purpose**  
   Describes the purpose of the loan, such as for a car, household, or education.

5. **Credit amount**  
   The amount of credit or loan being requested. This is a key feature for understanding the financial risk involved.

6. **Savings account/bonds**  
   Indicates the amount of savings or bonds held by the individual, used as a measure of financial stability.

7. **Present employment since**  
   The duration of the individual’s current employment, categorized into ranges, helping to assess job stability.

8. **Installment rate in percentage of disposable income**  
   The installment rate as a percentage of the individual’s disposable income, indicating the affordability of the loan.

9. **Personal status and sex**  
   Describes the individual’s marital status and gender, which may influence their credit risk assessment.

10. **Other debtors/guarantors**  
    Indicates whether there are other parties (e.g., guarantors) involved in the loan.

11. **Present residence since**  
    The number of years the individual has lived at their current residence, indicating residential stability.

12. **Property**  
    Describes the type of property owned, if any, such as real estate or other valuable assets.

13. **Age in years**  
    The age of the individual, which may influence credit risk, particularly at younger or older ages.

14. **Other installment plans**  
    Indicates if the individual has any other installment loans or payment plans, which can affect their ability to repay.

15. **Housing**  
    Describes the individual’s housing situation, such as renting or owning, which may impact financial stability.

16. **Number of existing credits at this bank**  
    The number of loans or credits the individual currently has with the same bank.

17. **Job**  
    The type of job held by the individual, categorized by job stability and security.

18. **Number of people being liable to provide maintenance for**  
    The number of people financially dependent on the individual, affecting disposable income.

19. **Telephone**  
    A binary feature indicating whether the individual has a registered telephone number, suggesting financial accessibility.

20. **Foreign worker**  
    A binary feature indicating whether the individual is a foreign worker, which can sometimes influence credit decisions.

21. **Credit risk (Good/Bad)**  
    The target variable classifying the individual as a good or bad credit risk based on the aforementioned features.

<br><br>

## MIMIC-IV.csv

### Dataset Overview
This dataset is part of the **MIMIC-IV (Medical Information Mart for Intensive Care IV)**, which is a large, freely accessible electronic health record (EHR) dataset containing de-identified health-related data of ICU patients. It includes structured data on demographics, vital signs, laboratory tests, diagnoses, medications, and more. Key features include patient age, gender, ethnicity, diagnoses, and procedures. MIMIC-IV is widely used in healthcare research, including studies on bias detection, especially regarding disparities in treatment outcomes across different demographic groups such as race and gender. This dataset is crucial for fairness-related health analytics.

### Citation
Johnson, A. E. W., Bulgarelli, L., Shen, L., Gayles, A., Shammout, A., Horng, S., Pollard, T. J., Hao, S., Moody, B., Gow, B., Lehman, L. W., Celi, L. A., & Mark, R. G. (2023). MIMIC-IV, a freely accessible electronic health record dataset. *Scientific Data*, 10(1), 1. [https://doi.org/10.1038/s41597-022-01899-x](https://doi.org/10.1038/s41597-022-01899-x)


### Feature Descriptions and Definitions

1. **admission_type (Admission Type)**  
   Describes how the patient was admitted to the hospital, such as through emergency, elective, or urgent care. This feature is key for understanding the different pathways through which patients receive care in ICU settings.

2. **hospital_expire_flag (Hospital Expiration Flag)**  
   A binary indicator (1 = deceased, 0 = survived) showing whether the patient passed away during hospitalization. Essential for analyzing mortality rates and overall treatment outcomes.

3. **admission_location (Admission Location)**  
   Identifies the source of the patient's admission, such as from the emergency department, clinic referral, or transfer from another hospital. This information helps analyze patient flow and utilization of healthcare services.

4. **discharge_location (Discharge Location)**  
   Indicates where the patient was discharged, such as home, rehabilitation centers, or to another hospital. It provides insights into healthcare transitions and patient recovery outcomes.

5. **patient_insurance (Patient Insurance Type)**  
   Specifies the patient’s insurance coverage, such as Medicare, Medicaid, private insurance, or self-pay. This is critical for studying how financial resources influence access to healthcare and outcomes.

6. **patient_lang (Patient Language)**  
   The primary language spoken by the patient. This feature is important for assessing the impact of language barriers on patient care and communication in healthcare settings.

7. **patient_marital (Patient Marital Status)**  
   Indicates the patient's marital status (e.g., single, married, divorced), which may influence social support and patient outcomes in healthcare.

8. **patient_race (Patient Race)**  
   Records the race or ethnicity of the patient, essential for analyzing racial disparities in healthcare access, treatment, and outcomes.

9. **patient_gender (Patient Gender)**  
   The gender of the patient, typically recorded as male or female. Important for analyzing gender-related differences in healthcare outcomes and clinical interventions.

10. **patient_age (Patient Age)**  
    Records the age of the patient. This is a fundamental demographic variable for studying age-related health trends, mortality rates, and the prevalence of chronic conditions.

<br><br>

## Student Performance.csv

### Dataset Overview
The **Student Performance** dataset, collected by **Paulo Cortez** in 2008, contains information on the academic performance of students in Portuguese schools. It includes various demographic, social, and academic attributes, with the primary goal of predicting students' final grades. The dataset includes student performance in Mathematics, and is often used in educational data mining research for tasks such as predicting student success, identifying factors affecting academic performance, and exploring the effects of different student behaviors and backgrounds on academic outcomes.

### Citation
Cortez, P. (2008). Student Performance [Dataset]. UCI Machine Learning Repository. [https://doi.org/10.24432/C5TG7T](https://doi.org/10.24432/C5TG7T)

### Feature Descriptions and Definitions

1. **school (School Name)**  
   The school the student attends, categorized as either "GP" (Gabriel Pereira) or "MS" (Mousinho da Silveira).

2. **sex (Gender)**  
   The gender of the student, recorded as "F" (female) or "M" (male).

3. **age (Age)**  
   The age of the student, given as an integer.

4. **address (Residence Location)**  
   The student’s living location, either "U" (urban) or "R" (rural).

5. **famsize (Family Size)**  
   Describes the size of the student's family, with "LE3" indicating fewer than three members and "GT3" indicating more than three members.

6. **Pstatus (Parent's Cohabitation Status)**  
   Indicates whether the student’s parents live together ("T" for together) or apart ("A" for apart).

7. **Medu (Mother’s Education)**  
   The education level of the student's mother, ranging from 0 (none) to 4 (higher education).

8. **Fedu (Father’s Education)**  
   The education level of the student's father, using the same 0–4 scale as Medu.

9. **Mjob (Mother’s Job)**  
   The occupation of the student's mother, categorized as "teacher," "health," "services," "at_home," or "other."

10. **Fjob (Father’s Job)**  
    The occupation of the student's father, with the same categories as Mjob.

11. **reason (Reason for School Choice)**  
    The reason the student chose their school, which could be "home" (close to home), "reputation," "course" (specific course offered), or "other."

12. **guardian (Guardian)**  
    The student's guardian, either "mother," "father," or "other."

13. **traveltime (Travel Time to School)**  
    The amount of time it takes for the student to travel to school, categorized as 1 (less than 15 minutes) to 4 (more than an hour).

14. **studytime (Weekly Study Time)**  
    The number of hours the student spends studying per week, categorized from 1 (less than 2 hours) to 4 (more than 10 hours).

15. **failures (Past Class Failures)**  
    The number of times the student has failed a class, with values ranging from 0 to 3.

16. **schoolsup (School Educational Support)**  
    Whether the student receives extra educational support at school, recorded as "yes" or "no."

17. **famsup (Family Educational Support)**  
    Whether the student receives extra educational support from family, recorded as "yes" or "no."

18. **paid (Extra Paid Classes)**  
    Whether the student attends extra paid classes within the course subject, recorded as "yes" or "no."

19. **activities (Extracurricular Activities)**  
    Whether the student participates in extracurricular activities, recorded as "yes" or "no."

20. **nursery (Attended Nursery School)**  
    Whether the student attended nursery school as a child, recorded as "yes" or "no."

21. **higher (Plans for Higher Education)**  
    Whether the student plans to pursue higher education, recorded as "yes" or "no."

22. **internet (Access to Internet)**  
    Whether the student has internet access at home, recorded as "yes" or "no."

23. **romantic (In a Romantic Relationship)**  
    Whether the student is currently in a romantic relationship, recorded as "yes" or "no."

24. **famrel (Family Relationship Quality)**  
    The quality of the student’s family relationships, rated from 1 (very bad) to 5 (excellent).

25. **freetime (Free Time after School)**  
    How much free time the student has after school, rated from 1 (very little) to 5 (a lot).

26. **goout (Going Out with Friends)**  
    How often the student goes out with friends, rated from 1 (very rarely) to 5 (very often).

27. **Dalc (Workday Alcohol Consumption)**  
    The amount of alcohol the student consumes on weekdays, rated from 1 (very low) to 5 (very high).

28. **Walc (Weekend Alcohol Consumption)**  
    The amount of alcohol the student consumes on weekends, rated from 1 (very low) to 5 (very high).

29. **health (Current Health Status)**  
    The current health status of the student, rated from 1 (very bad) to 5 (very good).

30. **absences (Number of Absences)**  
    The number of times the student was absent from school.

31. **G1 (First Period Grade)**  
    The student’s grade in the first grading period, ranging from 0 to 20.

32. **G2 (Second Period Grade)**  
    The student’s grade in the second grading period, ranging from 0 to 20.

33. **G3 (Final Grade)**  
    The student’s final grade, ranging from 0 to 20, which is the target variable for predictive modeling.




<br><br><br><br>

# Tasksets Table

|                | Distribution | Correlation | Implication | Total |
|----------------|--------------|-------------|----------------|-------|
| Adult.csv        |     11       |     9      |     6         |  26   |
| COMPAS.csv     |     8       |     8      |     5         |  21   |
| Statlog.csv        |      7       |      8      |      5         |  20   |
| MIMIC-IV.csv   |      6       |      6      |      6         |  18   |
| Student Performance.csv        |      5       |     8      |      2         |  15   |
| **Total**      |     37       |     39      |     24         | 100   |



<br><br>

## Adult.csv

### **Quantity of Questions: 11 distribution + 9 correlation + 6 not specified = 26**

| Question | Question Type | Related Feature(s) | Question Significance |
| -------- | ------------- | ------------------ | --------------------- |
| Can you check if the age distribution across individuals is balanced, or do certain age groups dominate? | distribution | age (Numerical) | An uneven age distribution could skew insights into income patterns across different age groups. |
| How does the distribution of work class look to you? Are there any work classes that appear to be overrepresented? | distribution | workclass (Categorical) | A skewed work class distribution may distort our understanding of income disparities across different employment sectors. |
| From your perspective, is the distribution of education levels spread fairly, or do certain levels dominate? | distribution | education (Categorical) | Education is closely tied to income potential, and an imbalanced distribution could introduce bias in analyzing the effects of education on earnings. |
| In your view, how does the marital status distribution appear? Are any marital statuses overrepresented? | distribution | marital-status (Categorical) | An uneven marital status distribution might distort the analysis of social and financial impacts on income. |
| Do certain occupations dominate the dataset, or is the distribution of occupations relatively even? | distribution | occupation (Categorical) | Since occupations heavily influence income, an unbalanced distribution might lead to biased conclusions about income differences between professions. |
| How do household roles seem to be distributed? Are there certain roles that are more prevalent than others? | distribution | relationship (Categorical) | Household relationships can affect family income dynamics, and a skewed distribution could introduce bias into the analysis of these relationships. |
| Could you tell if the racial distribution appears fair, or does one racial group dominate the data? | distribution | race (Categorical) | Racial imbalances could introduce bias when analyzing differences in income and employment opportunities across racial groups. |
| How balanced does the gender distribution look? Is one gender significantly more represented than the other? | distribution | sex (Categorical) | Gender imbalances could lead to biased conclusions when analyzing income differences and gender wage gaps. |
| What do you think about the distribution of weekly work hours? Are certain ranges more concentrated than others? | distribution | hours-per-week (Numerical) | Weekly working hours have a direct impact on income, and an uneven distribution could skew labor analysis. |
| Are there any notable patterns in the native country distribution, or is the dataset well-balanced in terms of geographic representation? | distribution | native-country (Categorical) | An imbalance in native countries could lead to biased insights into income differences based on nationality or geographic origin. |
| Is the income distribution balanced between individuals earning above and below $50K, or does one group dominate? | distribution | income (Categorical) | An uneven distribution of income classes could impact the analysis of income disparities and economic inequality. |
| -------- distribution above, correlation below -------- |
| Can you find any patterns between age and income? Do older individuals tend to earn more? | correlation | age (Numerical), income (Categorical) | Age could influence earning potential, and understanding this relationship is key to analyzing age-related income trends. |
| I need your assistance to explore if education and race might be influencing each other. Is there any noticeable connection? | correlation | education (Categorical), race (Categorical) | Racial disparities in education could reveal inequalities that impact overall opportunities and economic outcomes. |
| Help me understand if there’s a relationship between education levels and gender. Do certain education levels correlate with gender differences? | correlation | education (Categorical), sex (Categorical) | Gender differences in access to education may exist, and identifying this correlation can highlight educational disparities. |
| I’m curious, does educational attainment have a direct influence on income? Can you detect any trends here? | correlation | education (Categorical), income (Categorical) | Education is a primary driver of income, and this relationship can highlight the economic value of higher education. |
| Use your abilities to determine if race and occupation are connected in any meaningful way. Is there a pattern here? | correlation | occupation (Categorical), race (Categorical) | Racial bias may affect career paths and job opportunities, which could influence income inequality across professions. |
| What kind of relationship can you find between occupation and income? Do certain jobs tend to lead to higher earnings? | correlation | occupation (Categorical), income (Categorical) | Occupation is directly linked to income levels, and some professions may consistently offer higher financial rewards. |
| I need your help to see if there’s any connection between race and income in this dataset. Could certain racial groups be earning more than others? | correlation | race (Categorical), income (Categorical) | There may be significant racial income gaps, reflecting broader societal inequalities in economic opportunities. |
| Could you explore whether there is a noticeable link between gender and income? Is there a pay gap between men and women? | correlation | sex (Categorical), income (Categorical) | Gender-based income differences may highlight the extent of pay inequality between males and females. |
| Help me figure out if people’s native country impacts their income. Are individuals from certain countries more likely to earn higher wages? | correlation | native-country (Categorical), income (Categorical) | The country of origin might influence income, revealing disparities based on nationality or migration. |
| -------- correlation above, not specified below ------- |
| I need your assistance to see if age might be contributing to any bias in the dataset. Could there be any hidden effects here? | not specified | age (Numerical) | Age can subtly influence opportunities, and exploring any biases here helps promote fairness in decision-making. |
| Help me understand whether educational attainment has any unintended biases in how individuals are assessed or treated. | not specified | education (Categorical) | Education level might create unequal access to opportunities, and identifying bias could help balance these inequalities. |
| Use your abilities to detect any hidden biases associated with occupation. Could some jobs be unfairly favored? | not specified | occupation (Categorical) | Bias in occupational roles might affect career progression, and addressing these biases can create a more inclusive workplace. |
| I’m curious to know if race plays a role in influencing how individuals are perceived or treated. Could there be unnoticed bias here? | not specified | race (Categorical) | Racial perceptions might affect treatment or opportunity distribution, and identifying bias can help ensure racial equality. |
| Could you explore whether gender has any impact on decision-making or opportunity access? I’d like to see if any bias exists. | not specified | sex (Categorical) | Gender biases might shape career paths or opportunities, and uncovering them ensures equal treatment across genders. |
| I need your help to see if there’s any bias linked to an individual’s native country. Could nationality be influencing outcomes here? | not specified | native-country (Categorical) | Nationality could lead to unequal access to opportunities or benefits, and identifying such bias can help eliminate nationality-based discrimination. |



<br><br>

## COMPAS.csv

### **Quantity of Questions: 8 distribution + 8 correlation + 5 not specified = 21**

| Question | Question Type | Related Feature(s) | Question Significance |
| -------- | ------------- | ------------------ | --------------------- |
| I’d appreciate your help in determining whether there is a dominant agency performing assessments, or if the distribution of assessments across agencies is fairly even. | distribution | Agency_Text (Categorical) | A bias in agency distribution could indicate institutional preferences or unequal resource allocation. |
| Do you have any insights into how the gender balance looks in this dataset? Are there more males or females? | distribution | Sex_Code_Text (Categorical) | Gender imbalances might affect the fairness of gender-based criminal justice outcomes. |
| Can we look into whether one ethnicity stands out in the data, or are the various racial groups equally represented? | distribution | Ethnic_Code_Text (Categorical) | Overrepresentation of a particular race could lead to skewed analysis of racial disparities. |
| How might defendants' age distribution impact the analysis? Is it evenly spread across all age groups, or do certain age groups dominate? | distribution | DateOfBirth (Numerical) | Skewed age representation could bias analysis related to age and legal outcomes. |
| Could you find out if there's any noticeable trend regarding the most spoken languages among defendants? | distribution | Language (Categorical) | If certain languages dominate, it may suggest potential challenges for non-native speakers in the legal system. |
| Do you think the current legal status of defendants is fairly distributed, or is there an imbalance that could hint at bias? | distribution | LegalStatus (Categorical) | An uneven distribution of legal statuses might reflect underlying systemic biases. |
| In your view, does the custody status distribution seem balanced, or do certain statuses dominate? | distribution | CustodyStatus (Categorical) | Custody status imbalances might affect conclusions about defendant treatment across different custody levels. |
| How do you interpret the marital status distribution here? Do you see any indication of one group being overrepresented? | distribution | MaritalStatus (Categorical) | Marital status imbalance might reveal underlying social influences on legal decisions. |
| -------- distribution above, correlation below -------- |
| Could you help me figure out if gender has any influence on the recommended supervision levels? Is there a noticeable pattern? | correlation | Sex_Code_Text (Categorical) and RecSupervisionLevel (Numerical) | If gender plays a role in supervision levels, it could indicate bias in how male and female defendants are assessed. |
| I'm curious whether the assessment scores are influenced by gender? | correlation | Sex_Code_Text (Categorical) and ScoreText (Categorical) | A correlation between gender and score text could reveal gender biases in how scores are assigned. |
| How does ethnicity relate to the recommended supervision levels? Are certain ethnic groups more likely to receive higher or lower levels? | correlation | Ethnic_Code_Text (Categorical) and RecSupervisionLevelText (Categorical) | A disparity here could suggest that ethnicity is influencing the supervision level decisions, leading to unequal treatment. |
| Can you explore if ethnicity is correlated with decile scores? | correlation | Ethnic_Code_Text (Categorical) and DecileScore (Numerical) | A correlation between ethnicity and risk scores may indicate bias in the risk assessment algorithm. |
| Could you take a look at whether age is a factor in the supervision level recommendations? Are older or younger individuals treated differently? | correlation | DateOfBirth (Numerical) and RecSupervisionLevel (Numerical) | Age-related bias might lead to unequal supervision level recommendations for defendants in different age groups. |
| Is there any link between the birth dates of defendants and the decile scores they receive? Are certain age groups scored higher than others? | correlation | DateOfBirth (Numerical) and DecileScore (Numerical) | A correlation between age and decile scores could show potential bias in how risk is assessed based on age. |
| Help me understand if language has any bearing on the supervision levels recommended. | correlation | Language (Categorical) and RecSupervisionLevelText (Categorical) | Language-based biases could affect how defendants are supervised, possibly leading to unequal outcomes for non-native speakers. |
| Can you analyze whether the language spoken by defendants influences the assessment scores? Does one language group tend to score differently? | correlation | Language (Categorical) and ScoreText (Categorical) | A bias here could highlight challenges faced by non-native speakers in understanding or navigating the legal system. |
| -------- correlation above, not specified below ------- |
| What kind of potential bias might gender introduce in this dataset? | not specific | Sex_Code_Text (Categorical) | Gender bias could affect overall analysis and lead to unfair treatment of defendants. |
| Could there be some unnoticed bias related to ethnicity in this dataset? | not specific | Ethnic_Code_Text (Categorical) | Ethnic bias could result in unfair outcomes for certain racial groups in both data analysis and legal decisions. |
| Should we be concerned about any issues related to age in this dataset? | not specific | DateOfBirth (Numerical) | Age might influence certain results, potentially leading to differential treatment across age groups. |
| What hidden impact could language have within the system? | not specific | Language (Categorical) | Language differences might reveal underlying bias, especially affecting non-native speakers. |
| Is there any hidden influence of marital status we should be aware of? | not specific | MaritalStatus (Categorical) | Marital status could be a hidden factor in analysis or decisions, potentially introducing bias. |

<br><br>

## Statlog.csv

### **Quantity of Questions: 7 distribution + 8 correlation + 5 not specified = 20**

| Question | Question Type | Related Feature(s) | Question Significance |
| -------- | ------------- | ------------------ | --------------------- |
| Could you assess whether the distribution of checking account statuses is fair, or if certain account types are more frequently represented than others? | distribution | Status of existing checking account (Categorical) | Disproportionate distribution of checking account statuses could reflect unequal access to financial products, impacting credit risk assessments. |
| How evenly is the credit history of individuals distributed across the categories, and could this suggest any systemic bias in prior credit opportunities? | distribution | Credit history (Categorical) | A skewed distribution of credit history may reveal patterns of unequal access to credit or discriminatory lending practices in the past. |
| Is there any indication that one loan purpose dominates the dataset? | distribution | Purpose (Categorical) | Imbalances in loan purposes may reflect economic disparities or biases in the types of loans most frequently granted. |
| Does the dataset show a balanced distribution of employment duration, or are certain durations over-represented? | distribution | Present employment since (Categorical) | Skewed representation in employment duration could signal that lenders prefer individuals with specific employment histories, introducing bias into lending decisions. |
| Can you detect whether certain installment rates (as a percentage of disposable income) appear more often than others? | distribution | Installment rate in percentage of disposable income (Numerical) | Bias in installment rates may disproportionately impact borrowers with lower income, limiting their ability to access fair loan terms. |
| Could you explore if there’s an over-representation of certain types of other debtors or guarantors? Might this reveal patterns in how creditworthiness is supported or evaluated? | distribution | Other debtors/guarantors (Categorical) | Disproportionate reliance on specific types of guarantors or debtors might indicate bias in how financial support structures are used in credit decisions. |
| How fairly are foreign workers represented in the dataset? Is there a noticeable difference in their presence, and what could that imply about their access to credit? | distribution | Foreign worker (Categorical) | An imbalance in the representation of foreign workers could suggest discriminatory practices in credit availability for non-native populations. |
| -------- distribution above, correlation below -------- |
| I’d like to know if personal status and sex might have an impact on credit risk outcomes. Could you check if certain groups are more likely to face unfavorable decisions? | correlation | Personal status and sex (Categorical), Credit risk (Good/Bad) (Categorical) | This question could reveal gender or marital status biases, showing if certain demographics face challenges in receiving fair credit decisions. |
| Could you help me figure out if age correlates with credit risk? | correlation | Age in years (Numerical), Credit risk (Good/Bad) (Categorical) | Investigating this could show whether creditworthiness is influenced by age, which may suggest discriminatory practices against certain age groups. |
| I need your help to explore whether job type influences credit risk classification. Is there any meaningful relationship between profession and credit outcomes? | correlation | Job (Categorical), Credit risk (Good/Bad) (Categorical) | Understanding the link between job type and credit risk could highlight occupational biases in financial decisions. |
| Could foreign worker status be a factor in credit risk? | correlation | Foreign worker (Categorical), Credit risk (Good/Bad) (Categorical) | This could uncover potential biases against non-native individuals in credit risk assessments, suggesting possible systemic issues. |
| Can you assist me in determining whether installment rates as a percentage of disposable income relate to personal status and sex? Could this point to a bias in loan structuring? | correlation | Installment rate in percentage of disposable income (Numerical), Personal status and sex (Categorical) | Exploring this could reveal how financial burdens are distributed based on gender and marital status, potentially highlighting inequality. |
| Could you check if there’s a connection between an individual's credit history and their job type? Do certain professions align with better or worse credit histories? | correlation | Credit history (Categorical), Job (Categorical) | This might point to job-related biases, where certain occupations are predisposed to better or worse credit behavior. |
| Use your abilities to determine if foreign workers tend to have worse credit histories. | correlation | Credit history (Categorical), Foreign worker (Categorical) | This could reveal if there are disadvantages faced by foreign workers regarding credit access or their historical credit behavior. |
| Help me understand if the number of dependents has any bearing on credit risk. Is there any noticeable correlation between family size and credit outcomes? | correlation | Number of people being liable to provide maintenance for (Numerical), Credit risk (Good/Bad) (Categorical) | A skew here could suggest that individuals with larger families are treated differently in credit risk assessments, which may indicate a bias. |
| -------- correlation above, not specified below ------- |
| Could you help me check if there’s any potential bias related to personal status and sex? | not specific | Personal status and sex (Categorical) | This question broadly explores whether marital status or gender might be linked to bias. |
| I’m wondering if housing circumstances could be tied to any kind of bias. Can you take a look? | not specific | Housing (Categorical) | This question focuses on housing conditions and whether they might be associated with bias. |
| Could you assist me in understanding if job type might be associated with any bias? | not specific | Job (Categorical) | This question broadly explores whether job type could be linked to bias. |
| Is there a possibility that bias exists depending on whether someone has a telephone? Can you check that for me? | not specific | Telephone (Categorical) | This question examines whether the presence of a telephone might introduce bias. |
| Could you help me confirm if there’s any bias related to the type of property someone owns? | not specific | Property (Categorical) | This question seeks to explore any potential bias linked to property ownership. |



<br><br>

## MIMIC-IV.csv

### **Quantity of Questions: 6 distribution + 6 correlation + 6 not specified = 18**

| Question | Question Type | Related Feature(s) | Question Significance |
| -------- | ------------- | ------------------ | --------------------- |
| Can you assess whether the distribution of patient languages is fairly represented, or if any language dominates? | distribution | patient_lang (Categorical) | An imbalance in the representation of languages might reveal language barriers in healthcare, affecting communication and treatment outcomes. |
| Is there any indication that the marital status distribution is unbalanced? | distribution | patient_marital (Categorical) | An uneven distribution of marital statuses might affect the analysis of social support and recovery outcomes in patients. |
| Do you think the distribution of patient races looks reasonable, or is one race overrepresented? | distribution | patient_race (Categorical) | If one race is overrepresented, it could skew the understanding of racial disparities in healthcare access and outcomes. |
| Is the gender distribution balanced, or is one gender dominating the dataset? | distribution | patient_gender (Categorical) | A skewed gender distribution could influence the analysis of gender-related differences in treatment and clinical outcomes. |
| Could you take a look at whether the age distribution seems evenly spread, or if it's skewed toward certain age groups? | distribution | patient_age (Numerical) | Age plays a critical role in healthcare outcomes, and a skewed age distribution might introduce bias in analyzing age-related health trends. |
| Can you assess whether the various patient insurance types are well-represented, or is there an overrepresentation of a particular type? | distribution | patient_insurance (Categorical) | An uneven distribution of insurance types might indicate financial disparities in accessing healthcare, affecting treatment outcomes. |
| -------- distribution above, correlation below -------- |
| I’m interested to see if there’s any noticeable relationship between patient age and hospital mortality. Could you find any patterns here? | correlation | patient_age (Numerical), hospital_expire_flag (Categorical) | Age could significantly impact mortality rates during hospitalization, especially with older patients, which might introduce bias into treatment outcomes. |
| Can you explore if there’s any correlation between gender and mortality rates during hospitalization? | correlation | patient_gender (Categorical), hospital_expire_flag (Categorical) | Gender may play a crucial role in patient outcomes, and understanding this connection helps clarify gender-specific differences in healthcare results. |
| I need your assistance to see if race and insurance type might be influencing each other in this dataset. Could there be a link here? | correlation | patient_race (Categorical), patient_insurance (Categorical) | Different races might have varying access to certain types of insurance, reflecting economic or healthcare access disparities. |
| Use your abilities to determine if patient race and hospital mortality rates are connected in any meaningful way. | correlation | patient_race (Categorical), hospital_expire_flag (Categorical) | There could be racial disparities in mortality rates, and identifying this link is essential for understanding potential bias in medical care. |
| Could you check whether language barriers are affecting patient outcomes, especially regarding mortality? I’d like to see if language influences survival rates. | correlation | patient_lang (Categorical), hospital_expire_flag (Categorical) | Language differences may impact the quality of care and communication, potentially leading to higher mortality rates for non-native speakers. |
| Help me understand whether patient insurance type has any influence on hospital mortality. Is there a noticeable bias here? | correlation | patient_insurance (Categorical), hospital_expire_flag (Categorical) | Insurance types might affect the level of care patients receive, and any bias here could reveal financial inequalities in healthcare outcomes. |
| -------- correlation above, not specified below ------- |
| Can you help me figure out if there's any bias related to how language influences treatment? | Not Specified | patient_lang (Categorical) | Language barriers may affect how patients interact with healthcare providers, potentially leading to unequal treatment experiences. |
| Do you think marital status might subtly impact the decisions made during patient care? | Not Specified | patient_marital (Categorical) | Marital status might shape the level of social support and decision-making involvement in the treatment process. |
| Could race be creating any disparities in the care patients receive at this hospital? | Not Specified | patient_race (Categorical) | Racial differences might lead to unequal access to treatment or healthcare resources, reflecting potential bias. |
| Would you say gender plays a role in influencing treatment plans, perhaps introducing bias? | Not Specified | patient_gender (Categorical) | Gender differences may lead to varying treatment options being recommended, reflecting potential biases in care plans. |
| How might age affect decision-making and resource allocation during treatment? | Not Specified | patient_age (Numerical) | Age might influence how treatment is prioritized, potentially affecting the resources available to different age groups. |
| Could the type of insurance patients have be causing any unequal access to medical services? | Not Specified | patient_insurance (Categorical) | The type of insurance a patient has may affect the quality of care they receive, possibly leading to disparities in outcomes. |


<br><br>


## Student Performance.csv

### **Quantity of Questions: 5 distribution + 8 correlation + 2 not specified = 15**

| Question | Question Type | Related Feature(s) | Question Significance |
| -------- | ------------- | ------------------ | --------------------- |
| I’d like to explore whether students from urban and rural areas are evenly represented. Do you think the place of residence has any dominant pattern? | distribution | address (Categorical) | Investigating residence disparities might reveal location-based differences in student access to education, influencing academic outcomes. |
| Can you assess the balance in reasons why students choose their schools? Is there a trend that shows one factor, like proximity or reputation, standing out? | distribution | reason (Categorical) | Identifying a dominant reason for school choice could expose underlying influences, such as availability of certain programs or school reputation. |
| Can you use your insights to check if there’s an even spread in how much time students dedicate to study each week? | distribution | studytime (Categorical) | Understanding study time distribution might highlight differences in student academic discipline or preparation, which could affect overall performance. |
| Help me figure out if there’s a disproportionate number of students attending extra paid classes. | distribution | paid (Categorical) | Imbalances in paid class attendance may signal socio-economic factors influencing students' access to extra academic support. |
| I’m curious whether students report similar levels of family relationship quality. Can you check if there are significant differences in how they perceive their family relationships? | distribution | famrel (Categorical) | This question explores how home environments might vary among students, potentially impacting their social and academic outcomes. |
| -------- distribution above, correlation below -------- |
| Could there be a link between where students live (urban or rural) and their final grades? | correlation | address (Categorical), G3 (Numerical) | This relationship could uncover if geographical location influences student achievement, possibly due to varying access to educational resources. |
| Can you help me determine if the school a student attends affects their final grade?| correlation | school (Categorical), G3 (Numerical) | Understanding this correlation might reveal if specific schools provide a better learning environment, impacting student success. |
| I’m interested in whether receiving extra educational support from family plays a role in final grades. Is there a connection between family support and academic performance? | correlation | famsup (Categorical), G3 (Numerical) | This could highlight the importance of family involvement in a student's academic journey and its potential influence on their results. |
| Use your abilities to see if attending extra paid classes correlates with higher final grades. Is there any noticeable impact of paid classes on academic success? | correlation | paid (Categorical), G3 (Numerical) | This could show whether students who can afford extra paid classes achieve better grades, highlighting possible socio-economic disparities in education. |
| Can you analyze if having internet access at home is linked to better final grades? | correlation | internet (Categorical), G3 (Numerical) | This connection could reveal how access to online resources contributes to academic achievement, especially in the digital age. |
| Is there any correlation between family size and student performance? | correlation | famsize (Categorical), G3 (Numerical) | Family size might affect the level of attention or resources a student receives at home, influencing their academic outcomes. |
| Help me figure out if there’s a relationship between the reason students choose their school and their mother's education level. Does parental education play a role in school choice? | correlation | reason (Categorical), Medu (Numerical) | This might expose how parental education influences school selection, possibly reflecting socio-economic status and educational priorities. |
| I wonder if students who participate in extracurricular activities have parents with certain types of jobs. Is there a connection between student activities and their father's occupation? | correlation | activities (Categorical), Fjob (Categorical) | This could shed light on how parental occupation influences a student’s involvement in activities, possibly reflecting family priorities or time availability. |
| -------- correlation above, not specified below ------- |
| Can you help me explore whether students' plans for higher education show any particular patterns? | not specific | higher (Categorical) | Understanding students' intentions for pursuing higher education may reveal their long-term academic and career aspirations. |
| I’m curious about how being in a romantic relationship might affect students. Could you help me find any general trends? | not specific | romantic (Categorical) | Investigating the impact of romantic relationships on students may provide insights into how personal life influences their academic or social development. |