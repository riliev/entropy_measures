
require(dplyr)
DATA_PATH = "/home/rumen/github_data/reversed_enthropy/"
file_path =  paste0(DATA_PATH ,"models_1_2.txt")

dat =read.csv(file_path, sep = ",", header = FALSE, stringsAsFactors = FALSE)
names(dat) <- c("token","forward", "backward", "freq")
dat$freq <-  log(dat$freq,10)
dat$word_length <- NA
for (j in 1:length(dat$word_length)) {
  dat$word_length[j] <- nchar(dat$token[j])
}


#filter our low entropies due to low data
#dat = dat[dat$freq > 1,]
#dat = dat[dat$backward > 1 & dat$forward > 1,]
plot(dat$backward, dat$forward)
fit1 <- lm(word_length ~ freq + forward + backward, data= dat)
summary(fit1)
cor.test(dat$freq, dat$word_length)
cor.test(dat$forward, dat$word_length)
cor.test(dat$backward, dat$word_length)
cor.test(dat$backward, dat$forward)
cor.test(dat$backward, dat$freq)
cor.test(dat$freq, dat$forward)
fit1 <- lm( forward ~ freq  + word_length, data= dat)
summary(fit1)
forward.resid <- resid(fit1) 
fit1 <- lm( backward ~ freq  + word_length, data= dat)
backward.resid <- resid(fit1) 
plot(dat$backward,dat$freq)

