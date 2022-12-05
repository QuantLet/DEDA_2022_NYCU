
library(dplyr)
library(tidyverse)
library(lubridate) #date
library(magrittr)
library(readxl)
library(readr) #read csv
library(data.table) #loading big data
library(plyr)
library(haven)
library(zoo)

getwd()

trends_d <- read_csv('Pfizer_trends.csv') %>% select(1,3) 
colnames(trends_d) <- c('date','day')
trends_w <- read_csv('Pfizer_trends_week.csv') %>% select(1,3) 
colnames(trends_w) <- c('date','week')
trends <- trends_d %>% left_join(trends_w) %>% 
  mutate(test = na.locf(week,na.rm=FALSE,fromLast = TRUE), 
         trends = day*test/100) %>% 
  select(date, trends)
stock <- read_csv("Pfizer_StockPrice.csv") %>% select(-1) %>% rename(c('Adj Close' = 'AdjClose'))
score1 <- read_csv("Pfizer_Story_sentiment.csv") %>% select(-1) %>% rename(c('news_time' = 'Date')) 
score2 <- read_csv("Pfizer_Press_sentiment.csv") %>% select(-1) %>% rename(c('news_time' = 'Date')) 
score <- rbind(score1, score2) %>% filter(!is.na(Positive)) %>% 
  arrange(desc(Date), desc(Positive) ) %>% 
  mutate(dup = duplicated(Date)) %>%
  filter(dup == FALSE) %>% select(-dup)
tag <- data.frame(tag = c('Management', 'Research', 'Finance', 'Pandemic','Breaking News'), 
                  tag_n = 1:5)
data <- stock %>% 
  left_join(score) %>% rename(c('Date' = 'date')) %>% 
  left_join(trends) %>%
  mutate(year = year(date), month = month(date), 
         vol = log(Volume+1, base = exp(1)),
         vary = High - Low, 
         jump = Close - Open, 
         win = ifelse(jump > 0, 1,0),
         return = AdjClose - lag(AdjClose, n=1),
         release = ifelse(!is.na(Positive), 1, 0),
         positive = Positive/100,
         negative = Negative/100,
         tag = ifelse(news_tag %in% c('Finance', 'Financial', 'Investments'), 'Finance', 
                      ifelse(news_tag %in% c('Partnerships', 'Leadership', 'Responsibility','Hiring & Recruitment',
                                             'Health Equity', 'Government','Employees', 'Events'), 'Management', 
                             ifelse(news_tag %in% c('Research', 'Medicines', 'Prescription Medicines','Research and Pipeline',
                                                    'Clinical Trials', 'Maternal Immunization'), 'Research', 
                                    ifelse(news_tag %in% c('Vaccines','COVID-19'), 'Pandemic', news_tag ) ))),
         half = ifelse(month<7, 0, 1)
  ) %>% 
  left_join(tag) 
write.csv(data,file="Pfizer_data.csv",quote=T,row.names = F)


# all 
vary = lm(vary~release, data = data) #Create the linear regression
summary(vary)
jump = lm(jump~release, data = data) #Create the linear regression
summary(jump)
return = lm(return~release, data = data) #Create the linear regression
summary(return)


# vary
a1 <- data %>% filter(year == 2018)
vary18 = lm(vary~release+positive+negative+Polarity+Subjectivity, data = a1) #Create the linear regression
a1 <- data %>% filter(year == 2019)
vary19 = lm(vary~release+positive+negative+Polarity+Subjectivity, data = a1) #Create the linear regression
a1 <- data %>% filter(year == 2020)
vary20 = lm(vary~release+positive+negative+Polarity+Subjectivity, data = a1) #Create the linear regression
a1 <- data %>% filter(year == 2021)
vary21 = lm(vary~release+positive+negative+Polarity+Subjectivity, data = a1) #Create the linear regression
a1 <- data %>% filter(year == 2022)
vary22 = lm(vary~release+positive+negative+Polarity+Subjectivity, data = a1) #Create the linear regression

