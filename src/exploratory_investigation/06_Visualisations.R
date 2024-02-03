pacman::p_load(tidyverse)

# Remember to set working directory

# INTRODUCTION AND METHODS VISUALIZATION
df <- read.csv2("Folketingsmedlemmer.csv")

### Calculating means and standard deviations of age by group
df$Age <- as.numeric(df$Age)
mean(df$Age)
sd(df$Age)

female <- df %>% 
  filter(Female == 1)
mean(female$Age)
sd(female$Age)

male <- df %>% 
  filter(Female != 1) 
mean(male$Age)
sd(male$Age)

### Recode gender and make density plot
df2 <- df %>% 
  mutate(Gender = recode(Female, `1` = "Female",`0` = "Male"))

ggplot(df2, aes(x=Age, fill=Gender)) +
  geom_density(alpha=.4) +
  theme_bw()

### Visualising constituencies
df3 <- df2 %>% 
  group_by(Gender) %>% 
  count(Storkreds)

df2 <- df2 %>% 
  mutate(Storkreds = recode(Storkreds, 
                            "Vestjylland" = "Vestjyllands",
                            "Sydjylland" = "Sydjyllands",
                            "Sjælland" = "Sjællands",
                            "Østjylland" = "Østjyllands",
                            "Nordsjælland" = "Nordsjællands",
                            "Nordjylland" = "Nordjyllands",
                            "København omegn" = "Københavns Omegns",
                            "København" = "Københavns",
                            "Fyn" = "Fyns"))

df2 %>% ggplot(aes(x = Storkreds, fill = Gender)) +
  geom_bar(width = 0.4, alpha=.7) + 
  coord_flip() +
  theme_bw()

### Visualising training set datasizes
models <- data.frame(c("Radford et al. (2022)", "Chan et al. (2021)", "Narayanan et al. (2018)", "Likhomanenko (2021)"), c(680000,5140, 162000,305000))

colnames(models)[1] <- "paper"
colnames(models)[2] <- "hours"

pacman::p_load(scales)
models %>% ggplot(aes(x = paper, y = hours, fill = paper)) +
  geom_col(width = 0.4, alpha = 0.7) + 
  coord_flip() +
  theme_bw() +
  theme(legend.position = "none") +
  theme(axis.title.y=element_blank()) +
  labs(y = "Hours of training data") +
  scale_y_continuous(labels = label_comma())
