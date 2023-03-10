# -*- coding: utf-8 -*-
"""
Created on 2021

@author: Administrator
"""

#%%

# =============================================================================
# =============================================================================
# # 문제 01 유형(DataSet_01.csv 이용)
#
# 구분자 : comma(“,”), 4,572 Rows, 5 Columns, UTF-8 인코딩
# 
# 글로벌 전자제품 제조회사에서 효과적인 마케팅 방법을 찾기
# 위해서 채널별 마케팅 예산과 매출금액과의 관계를 분석하고자
# 한다.
# 컬 럼 / 정 의  /   Type
# TV   /     TV 마케팅 예산 (억원)  /   Double
# Radio / 라디오 마케팅 예산 (억원)  /   Double
# Social_Media / 소셜미디어 마케팅 예산 (억원)  / Double
# Influencer / 인플루언서 마케팅
# (인플루언서의 영향력 크기에 따라 Mega / Macro / Micro / 
# Nano) / String

# SALES / 매출액 / Double
# =============================================================================
# =============================================================================

import pandas as pd
import numpy as np

data1=pd.read_csv('Dataset_01.csv')

data1.info()





#%%

# =============================================================================
# 1. 데이터 세트 내에 총 결측값의 개수는 몇 개인가? (답안 예시) 23
# =============================================================================

# 결측치 체크
data1.isna().sum(axis=1)
data1.isna().sum().sum()

# 답: 26

# 참고

data1[data1.TV.isna().values]
data1.loc[data1.TV.isna()]

data1.dropna(axis=1, how = 'any')

data1[data1.isna().sum(axis=1) < 3]




#%%

# =============================================================================
# 2. TV, Radio, Social Media 등 세 가지 다른 마케팅 채널의 예산과 매출액과의 상관분석을
# 통하여 각 채널이 매출에 어느 정도 연관이 있는지 알아보고자 한다. 
# - 매출액과 가장 강한 상관관계를 가지고 있는 채널의 상관계수를 소수점 5번째
# 자리에서 반올림하여 소수점 넷째 자리까지 기술하시오. (답안 예시) 0.1234
# =============================================================================

data1.dtypes
data1.dtypes != 'object'
num_list = data1.columns[data1.dtypes != 'object']

q2 = data1.corr()['Sales'].drop('Sales').abs()
round(q2.max(),4)

# 답 : 09995

# 참고
q2.max() # 최대값
q2.idxmax() # 최대값의 인덱스명을 리턴
q2.nlargest(2) # 상위 k개의 값과 인덱스명을 리턴


a1 = data1.groupby('Influencer')
dir(a1)

a1.groups

a1.get_group('Macro')

data1.groupby('Influencer').apply(
    lambda x : x.corr()['Sales'].drop('Sales').abs().idxmax())


import seaborn as sns

a1 = data1.corr().abs()
sns.heatmap(a1)



#%%

# =============================================================================
# 3. 매출액을 종속변수, TV, Radio, Social Media의 예산을 독립변수로 하여 회귀분석을
# 수행하였을 때, 세 개의 독립변수의 회귀계수를 큰 것에서부터 작은 것 순으로
# 기술하시오. 
# - 분석 시 결측치가 포함된 행은 제거한 후 진행하며, 회귀계수는 소수점 넷째 자리
# 이하는 버리고 소수점 셋째 자리까지 기술하시오. (답안 예시) 0.123
# =============================================================================



from sklearn.linear_model import LinearRegression 
# 결측치, 변수순서 일치, 변주형 사용 못함, 상수와 회귀계수 리턴

from statsmodels.formula.api import  ols
# 결측치 제거, 순서 관계 없음(데이터프레임 방식 채택, 이름조회), 
# 범주형 사용(자동 더미 변환), 가설 검정에서 사용되는 모든 통계량 리턴

var_list = ['TV', 'Radio', 'Social_Media']
q3=data1.dropna()
lm1 = LinearRegression(fit_intercept = True)
lm1.fit(q3[var_list], data1['Sales'])

dir(lm1)
q2_ans =  pd.Series(lm1.coef_, index = var_list).sort_values()(ascending = False)

np.trunc(q2_ans * 1000) / 1000 # 소수점 셋째 자리까지는 살림

# 답: TV   3.562 Social_Media  0.004, Radio   -0.003



# 참고
#lm1.fit(q3['TV'].values.reshape(-1,1), data1['Sales'])
lm1.fit(q3['TV'], data1['Sales'])

q3['TV'].values.reshape(-1,1)
q3['TV'].ndim
q3['TV'].shape

q3[['TV']].ndim
q3[['TV']].shape


####

#1. 이상치
#2. 결측치
#3. 회귀분석

####

# (2) ols 적용

#ols('식', 데이터셋) # 회귀식 선언
#ols().fit() # 학습 진행

#ols('식', 데이터셋)
#식: 'y~x1+x2+x3-1'
#= '-1' : 상수항 제외
#- C() : 범주형 변수로 선언 -> 자동적으로 더미변수로 변환


lm2 = ols('Sales~TV+Social_Media', data1)
lm3 = lm2.fit()

dir(lm3)

lm3.summary()


#lm4 = ols('Sales~TV+Social_Media', data1).fit()

from sklearn.linear_model import LinearRegression
from statsmodels.formula.api import ols
from statsmodels.api import OLS, add_constant # 상수항 추가

# 1. LinearRegression

var_list=['TV', 'Radio', 'Social_Media']

q3=data1.dropna()
lm1=LinearRegression(fit_intercept=True).fit(q3[var_list], q3['Sales'])

dir(lm1)

lm1.coef_  # 회귀계수
lm1.intercept_ # 절편

coef1=pd.Series(lm1.coef_, index=var_list)
(np.floor(coef1.sort_values(ascending=False) * 1000) / 1000).values

# 답: 3.562,  0.004, -0.004

# 2. ols
# ols1=ols('y~x1+x2+C(cat1)-1', 데이터셋명)
# ols2=ols1.fit()

form1='Sales~TV+Radio+Social_Media'

lm2=ols(form1, q3).fit()

dir(lm2)
lm2.summary()
lm2.params
# 이상치 제외한 데이터
outlier_drop_data=q3[lm2.outlier_test()['bonf(p)'] >= 0.05] # 이상치 제외한 데이터
lm2.rsquared

lm2.pvalues.index[lm2.pvalues < 0.05] # 이상치 데이터 추출

lm2.params # 상수, 회귀계수
lm2.pvalues # t p-value

sel_var_list = lm2.pvalues.index[lm2.pvalues < 0.05]

'+'.join(var_list) # 'TV+Radio+Social_Media'

'Sales~TV-1'

'Sales~' + 'TV' + '-1'

form1 = 'Sales~' + '+'.join(var_list) + '-1'
form1 # 'Sales~TV-1'

lm5=ols(form1, q3).fit()
lm5.summary()

lm2_pred = lm2.predict(q3)
lm5_pred = lm5.predict(q3)

from sklearn.metrics import mean_absolute_error, mean_squared_error

mae3 = mean_absolute_error(q3.Sales, lm2_pred)
mae5 = mean_absolute_error(q3.Sales, lm5_pred)

mae3, mae5
# (2.3645272000944226, 2.3652415128017896)

from statsmodels.stats.outliers_influence import variance_inflation_factor

# 표준화, 입력 변수만 대상, 변수별로 위치번호

# variance_influence_factor(x변수데이터셋(array), 인덱스번호)

[variance_inflation_factor(q3[var_list].values, i) for i in range(3)]




# # 3. OLS : 상수항 미포함

# xx=add_constant(q3[var_list])
# lm4=OLS(q3['Sales'], xx).fit()

# lm4.summary()

# # 범주형
# var_list=q3.columns.drop('Sales')
# form2='Sales~' + '+'.join(var_list)

# lm5=ols(form2, q3).fit()

# lm5.summary()
# q3.Influencer.unique()






#%%

# =============================================================================
# =============================================================================
# # 문제 02 유형(DataSet_02.csv 이용)
# 구분자 : comma(“,”), 200 Rows, 6 Columns, UTF-8 인코딩

# 환자의 상태와 그에 따라 처방된 약에 대한 정보를 분석하고자한다
# 
# 컬 럼 / 정 의  / Type
# Age  / 연령 / Integer
# Sex / 성별 / String
# BP / 혈압 레벨 / String
# Cholesterol / 콜레스테롤 레벨 /  String
# Na_to_k / 혈액 내 칼륨에 대비한 나트륨 비율 / Double
# Drug / Drug Type / String
# =============================================================================
# =============================================================================

data2 = pd.read_csv('Dataset_02.csv')

data2.info()

data2.columns


#%%

# =============================================================================
# 1.해당 데이터에 대한 EDA를 수행하고, 여성으로 혈압이 High, Cholesterol이 Normal인
# 환자의 전체에 대비한 비율이 얼마인지 소수점 네 번째 자리에서 반올림하여 소수점 셋째
# 자리까지 기술하시오. (답안 예시) 0.123
# =============================================================================

q1 = data2[['Sex', 'BP', 'Cholesterol']].value_counts(normalize=True)

q1.index
q1[('F', 'HIGH', 'NORMAL')]
# # 답 : 0.105

# q1 = q1.reset_index()
q1.droplevel(0)

#%%

# =============================================================================
# 2. Age, Sex, BP, Cholesterol 및 Na_to_k 값이 Drug 타입에 영향을 미치는지 확인하기
# 위하여 아래와 같이 데이터를 변환하고 분석을 수행하시오. 
# - Age_gr 컬럼을 만들고, Age가 20 미만은 ‘10’, 20부터 30 미만은 ‘20’, 30부터 40 미만은
# ‘30’, 40부터 50 미만은 ‘40’, 50부터 60 미만은 ‘50’, 60이상은 ‘60’으로 변환하시오. 
# - Na_K_gr 컬럼을 만들고 Na_to_k 값이 10이하는 ‘Lv1’, 20이하는 ‘Lv2’, 30이하는 ‘Lv3’, 30 
# 초과는 ‘Lv4’로 변환하시오.
# - Sex, BP, Cholesterol, Age_gr, Na_K_gr이 Drug 변수와 영향이 있는지 독립성 검정을
# 수행하시오.
# - 검정 수행 결과, Drug 타입과 연관성이 있는 변수는 몇 개인가? 연관성이 있는 변수
# 가운데 가장 큰 p-value를 찾아 소수점 여섯 번째 자리 이하는 버리고 소수점 다섯
# 번째 자리까지 기술하시오.
# (답안 예시) 3, 1.23456
# =============================================================================

# 범주형 변수들끼리 독립성 검정 : 카이스퀘어 검정

# (1) 카이스퀘어 검정 순서
# - 교차표 작성
# - 카이스퀘어 검정 수행(입력값을 교차표로 작성해서 삽입)
# - 가설
# H0: 두 변수가 독립이다 vs H1: 두 변수가 독립이 아니다(상관이 있다)

# (2) 분석 순서
# 수치형 변수를 범주형 변수로 변경
# 카이스크퀘어 검정을 수행
# : 반복적으로 카이스퀘어 검정을 수행


# - 수치형 변수를 범주형 변수로 변경

# - Age_gr 컬럼을 만들고, Age가 20 미만은 ‘10’, 20부터 30 미만은 ‘20’, 30부터 40 미만은
# ‘30’, 40부터 50 미만은 ‘40’, 50부터 60 미만은 ‘50’, 60이상은 ‘60’으로 변환하시오. 

q2 = data2.copy()

## np.where(조건) : 조건에 해당하는 index번호 리턴
## np.where(조건, 참, 거짓)

q2['Age_gr']=np.where(   
                q2['Age'] < 20, 10,
                    np.where(q2['Age'] < 30, 20,
                       np.where(q2['Age'] < 40, 30, 
                         np.where(q2['Age'] < 50, 40, 
                            np.where(q2['Age'] < 60, 50,  60)))))


q2['Age_gr']=np.where(q2['Age'].isna(), q2['Age'],   # np.nan
                np.where(q2['Age'] < 20, 10,
                    np.where(q2['Age'] < 30, 20,
                       np.where(q2['Age'] < 40, 30, 
                         np.where(q2['Age'] < 50, 40, 
                            np.where(q2['Age'] < 60, 50,  60))))))

q2

# - Na_K_gr 컬럼을 만들고 Na_to_k 값이 10이하는 ‘Lv1’, 20이하는 ‘Lv2’, 30이하는 ‘Lv3’, 30 
# 초과는 ‘Lv4’로 변환하시오.


q2['Na_K_gr'] = np.where(q2['Na_to_K'] <= 10, 'Lv1',
                            np.where(q2['Na_to_K'] <= 20, 'Lv2',
                                     np.where(q2['Na_to_K'] <= 30, 'Lv3', 'Lv4')))
q2


# 카이스크퀘어 검정을 수행
# : 반복적으로 카이스퀘어 검정을 수행

# - Sex, BP, Cholesterol, Age_gr, Na_K_gr이 Drug 변수와 영향이 있는지 독립성 검정을
# 수행하시오.



from scipy.stats import chi2_contingency

var_list = ['Sex', 'BP', 'Cholesterol', 'Age_gr', 'Na_K_gr']

q2_out = []

for i in var_list:
    tab = pd.crosstab(index =q2[i], columns = q2['Drug'])
    chi2_out = chi2_contingency(tab)
    pvalue = chi2_out[1]
    q2_out.append([i, pvalue, chi2_out[0]])

q2_out = pd.DataFrame(q2_out, columns = ['var', 'pvalue', 'chi2'])
q2_out
# - 검정 수행 결과, Drug 타입과 연관성이 있는 변수는 몇 개인가?
q2_out2_drug = [q2_out.pvalue < 0.05]
q2_out2_drug

# 답 : 4

# 가운데 가장 큰 p-value를 찾아 소수점 여섯 번째 자리 이하는 버리고 소수점 다섯
# 번째 자리까지 기술하시오.

np.trunc(q2_out.pvalue.max() * 100000) / 100000

# 답 : 0.71383




#%%

# =============================================================================
# 3.Sex, BP, Cholesterol 등 세 개의 변수를 다음과 같이 변환하고 의사결정나무를 이용한
# 분석을 수행하시오.
# - Sex는 M을 0, F를 1로 변환하여 Sex_cd 변수 생성
# - BP는 LOW는 0, NORMAL은 1 그리고 HIGH는 2로 변환하여 BP_cd 변수 생성
# - Cholesterol은 NORMAL은 0, HIGH는 1로 변환하여 Ch_cd 생성
# - Age, Na_to_k, Sex_cd, BP_cd, Ch_cd를 Feature로, Drug을 Label로 하여 의사결정나무를
# 수행하고 Root Node의 split feature와 split value를 기술하시오. 
# 이 때 split value는 소수점 셋째 자리까지 반올림하여 기술하시오. (답안 예시) Age, 
# 12.345
# =============================================================================

# 범주형 변수를 수치화

q3 = data2.copy()

# - Sex는 M을 0, F를 1로 변환하여 Sex_cd 변수 생성
q3['Sex_cd'] = np.where(q3['Sex'] == 'M', 0, 1)

# - BP는 LOW는 0, NORMAL은 1 그리고 HIGH는 2로 변환하여 BP_cd 변수 생성
q3['BP_cd'] = np.where(q3['BP'] == 'LOW', 0,
                        np.where(q3['BP'] == 'NORMAL', 1, 2))

# - Cholesterol은 NORMAL은 0, HIGH는 1로 변환하여 Ch_cd 생성
q3['Ch_cd'] = np.where(q3['Cholesterol'] == 'NORMAL', 0,1)

# - Age, Na_to_k, Sex_cd, BP_cd, Ch_cd를 Feature로, Drug을 Label로 하여 의사결정나무를
# 수행하고 Root Node의 split feature와 split value를 기술하시오. 
# 이 때 split value는 소수점 셋째 자리까지 반올림하여 기술하시오.
var_list = ['Age', 'Na_to_K', 'Sex_cd', 'BP_cd', 'Ch_cd']

from sklearn.tree import DecisionTreeClassifier, plot_tree, export_text

dt = DecisionTreeClassifier().fit(q3[var_list], q3['Drug'])

dir(dt)

print(plot_tree(dt, feature_names=var_list, class_names= dt.classes_, fontsize=7, max_depth=2))

print(export_text(dt, feature_names=var_list))

# 이 때 split value는 소수점 셋째 자리까지 반올림하여 기술하시오.

# 답: Na_to_K ,  14.829

q3_imp = pd.Series(dt.feature_importances_, index=var_list)

q3_imp.sort_values(ascending = False).cumsum()


# 정확도(accuracy), 재현율(recall), 정밀도(precision)

from sklearn.metrics import confusion_matrix, classification_report, recall_score

q3_pred = dt.predict(q3[var_list])

print(confusion_matrix(q3['Drug'], q3_pred))

print(classification_report(q3["Drug"], q3_pred))

# recall_score(q3["Drug"], q3_pred, pos_label='DrugY')


#%%

# =============================================================================
# =============================================================================
# # 문제 03 유형(DataSet_03.csv 이용)
# 
# 구분자 : comma(“,”), 5,001 Rows, 8 Columns, UTF-8 인코딩
# 안경 체인을 운영하고 있는 한 회사에서 고객 사진을 바탕으로 안경의 사이즈를
# 맞춤 제작하는 비즈니스를 기획하고 있다. 우선 데이터만으로 고객의 성별을
# 파악하는 것이 가능할 지를 연구하고자 한다.
#
# 컬 럼 / 정 의 / Type
# long_hair / 머리카락 길이 (0 – 길지 않은 경우 / 1 – 긴
# 경우) / Integer
# forehead_width_cm / 이마의 폭 (cm) / Double
# forehead_height_cm / 이마의 높이 (cm) / Double
# nose_wide / 코의 넓이 (0 – 넓지 않은 경우 / 1 – 넓은 경우) / Integer
# nose_long / 코의 길이 (0 – 길지 않은 경우 / 1 – 긴 경우) / Integer
# lips_thin / 입술이 얇은지 여부 0 – 얇지 않은 경우 / 1 –
# 얇은 경우) / Integer
# distance_nose_to_lip_long / 인중의 길이(0 – 인중이 짧은 경우 / 1 – 인중이
# 긴 경우) / Integer
# gender / 성별 (Female / Male) / String
# =============================================================================
# =============================================================================

data3 = pd.read_csv('Dataset_03.csv')

data3.info()


#%%

# =============================================================================
# 1.이마의 폭(forehead_width_cm)과 높이(forehead_height_cm) 사이의
# 비율(forehead_ratio)에 대해서 평균으로부터 3 표준편차 밖의 경우를 이상치로
# 정의할 때, 이상치에 해당하는 데이터는 몇 개인가? (답안 예시) 10
# =============================================================================

q1 = data3.copy()

q1['forehead_ratio'] = q1['forehead_width_cm'] / q1['forehead_height_cm']

xbar = q1['forehead_ratio'].mean()
sd = q1['forehead_ratio'].std()

LB = xbar - (3 * sd)
UB = xbar + (3 * sd)

(q1['forehead_ratio'] < LB) | (q1['forehead_ratio'] > UB)

((q1['forehead_ratio'] < LB) | (q1['forehead_ratio'] > UB)).sum()

# 답 : 3


#%%

# =============================================================================
# 2.성별에 따라 forehead_ratio 평균에 차이가 있는지 적절한 통계 검정을 수행하시오.
# - 검정은 이분산을 가정하고 수행한다.
# - 검정통계량의 추정치는 절대값을 취한 후 소수점 셋째 자리까지 반올림하여
# 기술하시오.
# - 신뢰수준 99%에서 양측 검정을 수행하고 결과는 귀무가설 기각의 경우 Y로, 그렇지
# 않을 경우 N으로 답하시오. (답안 예시) 1.234, Y
# =============================================================================

from scipy.stats import bartlett, ttest_ind

q2_m = q1[q1.gender == 'Male']['forehead_ratio']
q2_f = q1[q1.gender == 'Female']['forehead_ratio']

ttest_ind(q2_m, q2_f, equal_var = False)

# 답: 2.999, Y











#%%

# =============================================================================
# 3.주어진 데이터를 사용하여 성별을 구분할 수 있는지 로지스틱 회귀분석을 적용하여
# 알아 보고자 한다. 
# - 데이터를 7대 3으로 나누어 각각 Train과 Test set로 사용한다. 이 때 seed는 123으로
# 한다.
# - 원 데이터에 있는 7개의 변수만 Feature로 사용하고 gender를 label로 사용한다.
# (forehead_ratio는 사용하지 않음)
# - 로지스틱 회귀분석 예측 함수와 Test dataset를 사용하여 예측을 수행하고 정확도를
# 평가한다. 이 때 임계값은 0.5를 사용한다. 
# - Male의 Precision 값을 소수점 둘째 자리까지 반올림하여 기술하시오. (답안 예시) 
# 0.12
# 
# 
# (참고) 
# from sklearn.linear_model import LogisticRegression
# from sklearn.model_selection import train_test_split
# from sklearn import metrics
# train_test_split 의 random_state = 123
# =============================================================================














#%%

# =============================================================================
# =============================================================================
# # 문제 04 유형(DataSet_04.csv 이용)
#
#구분자 : comma(“,”), 6,718 Rows, 4 Columns, UTF-8 인코딩

# 한국인의 식생활 변화가 건강에 미치는 영향을 분석하기에 앞서 육류
# 소비량에 대한 분석을 하려고 한다. 확보한 데이터는 세계 각국의 1인당
# 육류 소비량 데이터로 아래와 같은 내용을 담고 있다.

# 컬 럼 / 정 의 / Type
# LOCATION / 국가명 / String
# SUBJECT / 육류 종류 (BEEF / PIG / POULTRY / SHEEP) / String
# TIME / 연도 (1990 ~ 2026) / Integer
# Value / 1인당 육류 소비량 (KG) / Double
# =============================================================================
# =============================================================================

# (참고)
# #1
# import pandas as pd
# import numpy as np
# #2
# from scipy.stats import ttest_rel
# #3
# from sklearn.linear_model import LinearRegression

#%%

# =============================================================================
# 1.한국인의 1인당 육류 소비량이 해가 갈수록 증가하는 것으로 보여 상관분석을 통하여
# 확인하려고 한다. 
# - 데이터 파일로부터 한국 데이터만 추출한다. 한국은 KOR로 표기되어 있다.
# - 년도별 육류 소비량 합계를 구하여 TIME과 Value간의 상관분석을 수행하고
# 상관계수를 소수점 셋째 자리에서 반올림하여 소수점 둘째 자리까지만 기술하시오. 
# (답안 예시) 0.55
# =============================================================================







#%%

# =============================================================================
# 2. 한국 인근 국가 가운데 식생의 유사성이 상대적으로 높은 일본(JPN)과 비교하여, 연도별
# 소비량에 평균 차이가 있는지 분석하고자 한다.
# - 두 국가의 육류별 소비량을 연도기준으로 비교하는 대응표본 t 검정을 수행하시오.
# - 두 국가 간의 연도별 소비량 차이가 없는 것으로 판단할 수 있는 육류 종류를 모두
# 적으시오. (알파벳 순서) (답안 예시) BEEF, PIG, POULTRY, SHEEP
# =============================================================================






#%%

# =============================================================================
# 3.(한국만 포함한 데이터에서) Time을 독립변수로, Value를 종속변수로 하여 육류
# 종류(SUBJECT) 별로 회귀분석을 수행하였을 때, 가장 높은 결정계수를 가진 모델의
# 학습오차 중 MAPE를 반올림하여 소수점 둘째 자리까지 기술하시오. (답안 예시) 21.12
# (MAPE : Mean Absolute Percentage Error, 평균 절대 백분율 오차)
# (MAPE = Σ ( | y - y ̂ | / y ) * 100/n ))
# 
# =============================================================================













#%%

# =============================================================================
# =============================================================================
# # 문제 05 유형(DataSet_05.csv 이용)
#
# 구분자 : comma(“,”), 8,068 Rows, 12 Columns, UTF-8 인코딩
#
# A자동차 회사는 신규 진입하는 시장에 기존 모델을 판매하기 위한 마케팅 전략을 
# 세우려고 한다. 기존 시장과 고객 특성이 유사하다는 전제 하에 기존 고객을 세분화하여
# 각 그룹의 특징을 파악하고, 이를 이용하여 신규 진입 시장의 마케팅 계획을 
# 수립하고자 한다. 다음은 기존 시장 고객에 대한 데이터이다.
#

# 컬 럼 / 정 의 / Type
# ID / 고유 식별자 / Double
# Age / 나이 / Double
# Age_gr / 나이 그룹 (10/20/30/40/50/60/70) / Double
# Gender / 성별 (여성 : 0 / 남성 : 1) / Double
# Work_Experience / 취업 연수 (0 ~ 14) / Double
# Family_Size / 가족 규모 (1 ~ 9) / Double
# Ever_Married / 결혼 여부 (Unknown : 0 / No : 1 / Yes : 2) / Double
# Graduated / 재학 중인지 여부 / Double
# Profession / 직업 (Unknown : 0 / Artist ~ Marketing 등 9개) / Double
# Spending_Score / 소비 점수 (Average : 0 / High : 1 / Low : 2) / Double
# Var_1 / 내용이 알려지지 않은 고객 분류 코드 (0 ~ 7) / Double
# Segmentation / 고객 세분화 결과 (A ~ D) / String
# =============================================================================
# =============================================================================


#(참고)
#1
# import pandas as pd
# #2
# from scipy.stats import chi2_contingency
# #3
# from sklearn.model_selection import train_test_split
# from sklearn import metrics
# from sklearn.tree import DecisionTreeClassifier
# from sklearn.tree import export_graphviz
# import pydot


#%%

# =============================================================================
# 1.위의 표에 표시된 데이터 타입에 맞도록 전처리를 수행하였을 때, 데이터 파일 내에
# 존재하는 결측값은 모두 몇 개인가? 숫자형 데이터와 문자열 데이터의 결측값을
# 모두 더하여 답하시오.
# (String 타입 변수의 경우 White Space(Blank)를 결측으로 처리한다) (답안 예시) 123
# =============================================================================

data5 = pd.read_csv('Dataset_05.csv')
data5.isnull().sum().sum()

# 답 : 1166

#%%

# =============================================================================
# 2.이어지는 분석을 위해 결측값을 모두 삭제한다. 그리고, 성별이 세분화(Segmentation)에
# 영향을 미치는지 독립성 검정을 수행한다. 수행 결과, p-value를 반올림하여 소수점
# 넷째 자리까지 쓰고, 귀무가설을 기각하면 Y로, 기각할 수 없으면 N으로 기술하시오. 
# (답안 예시) 0.2345, N
# =============================================================================

q2 = data5.dropna()

from scipy.stats import chi2_contingency

tab = pd.crosstab(index = q2['Gender'], columns = q2['Segmentation'])
print(tab)

chi2_out = chi2_contingency(tab)
print(chi2_out)
pvalue = chi2_out[1]

round(pvalue, 4)

# 0.0031 , Y



#%%

# =============================================================================
# 3.Segmentation 값이 A 또는 D인 데이터만 사용하여 의사결정 나무 기법으로 분류
# 정확도를
# 측정해 본다. 
# - 결측치가 포함된 행은 제거한 후 진행하시오.
# - Train대 Test 7대3으로 데이터를 분리한다. (Seed = 123)
# - Train 데이터를 사용하여 의사결정나무 학습을 수행하고, Test 데이터로 평가를
# 수행한다.
# - 의사결정나무 학습 시, 다음과 같이 설정하시오:
# • Feature: Age_gr, Gender, Work_Experience, Family_Size, 
#             Ever_Married, Graduated, Spending_Score
# • Label : Segmentation
# • Parameter : Gini / Max Depth = 7 / Seed = 123
# 이 때 전체 정확도(Accuracy)를 소수점 셋째 자리 이하는 버리고 소수점 둘째자리까지
# 기술하시오.
# (답안 예시) 0.12
# =============================================================================

from sklearn import metrics
from sklearn.tree import export_graphviz
# import pydot


q3 = data5.dropna()
q3 = q3[q3.Segmentation.isin(['A', 'D'])]
q3.Segmentation.value_counts()

from sklearn.model_selection import train_test_split

train, test = train_test_split(q3, test_size = 0.3, random_state=123)

var_list = ['Age_gr', 'Gender', 'Work_Experience', 'Family_Size', 
            'Ever_Married', 'Graduated', 'Spending_Score']

from sklearn.tree import DecisionTreeClassifier

dt = DecisionTreeClassifier(max_depth=7, random_state=123)

dt.fit(train[var_list], train['Segmentation'])

np.trunc(dt.score(test[var_list], test['Segmentation']) * 100) / 100

# 답 : 0.68


# %%
