#load topic models library
#install.packages("wordcloud")
library(wordcloud)
library(topicmodels)
 

#Set parameters for Gibbs sampling
burnin <- 4000
iter <- 2000
thin <- 500
seed <-list(2003,5,63,100001,765)
nstart <- 5
best <- TRUE

#Number of topics
k <- 10

#Run LDA using Gibbs sampling
ldaOut <-LDA(dtm,k, method="Gibbs", control=list(nstart=nstart, seed = seed, best=best, burnin = burnin, iter = iter, thin=thin))


#write out results
#docs to topics
ldaOut.topics <- as.matrix(topics(ldaOut))
write.csv(ldaOut.topics,file=paste("LDAGibbs",k,"DocsToTopics_tf.csv"))


#top 20 terms in each topic
ldaOut.terms <- as.matrix(terms(ldaOut,20))
write.csv(ldaOut.terms,file=paste("LDAGibbs",k,"TopicsToTerms_tf.csv"))


#probabilities associated with each topic assignment
topicProbabilities <- as.data.frame(ldaOut@gamma)
write.csv(topicProbabilities,file=paste("LDAGibbs",k,"TopicProbabilities_tf.csv"))


for(i in 1:k){
  topic <- 10
  df <- data.frame(term = ldaOut@terms, p = exp(ldaOut@beta[topic,]))
  df$term
  df <- df[order(-df$p),]
  df <- df[1:20,]
  df
  
  #visualising top 20 terms in each topic
  wordcloud(words = df$term,
            freq = df$p,
            max.words = 200,
            random.order = FALSE,
            rot.per = 0.35,
            colors=brewer.pal(8, "Dark2"))
}


