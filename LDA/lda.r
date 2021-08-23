#load topic models library
#install.packages("wordcloud")
library(wordcloud)
library(topicmodels)

# Lectura de archivo
c <- Corpus(DirSource("Aqu� va la direcci�n de su archivo"))
summary(c)

# Creaci�n de matriz tf-idf
# dtm <- DocumentTermMatrix(c, control=list(wordLengths=c(3,Inf),weighting = weightTfIdf))
dtm <- DocumentTermMatrix(c)
x<-as.matrix(dtm)
rownames(x) <- paste(substring(rownames(x),1,5))

# Establecer par�metros para el muestreo de Gibbs 
burnin <- 4000
iter <- 2000
thin <- 500
seed <-list(2003,5,63,100001,765)
nstart <- 5
best <- TRUE

# N�mero de t�picos
k <- 10

# Ejecuci�n de LDA usando muestreo de Gibbs
ldaOut <-LDA(dtm,k, method="Gibbs", control=list(nstart=nstart, seed = seed, best=best, burnin = burnin, iter = iter, thin=thin))


# Mostrar los resultados
# Documentos a t�picos
ldaOut.topics <- as.matrix(topics(ldaOut))
write.csv(ldaOut.topics,file=paste("LDAGibbs",k,"DocsToTopics_tf.csv"))


# Top 20 t�rminos por t�pico
ldaOut.terms <- as.matrix(terms(ldaOut,20))
write.csv(ldaOut.terms,file=paste("LDAGibbs",k,"TopicsToTerms_tf.csv"))


# Probabilidades asociadas con cada asignaci�n de t�pico
topicProbabilities <- as.data.frame(ldaOut@gamma)
write.csv(topicProbabilities,file=paste("LDAGibbs",k,"TopicProbabilities_tf.csv"))

# Nube de palabras
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