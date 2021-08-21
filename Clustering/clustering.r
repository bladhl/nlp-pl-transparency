#upload
#install.packages("tm")
#install.packages("qdap")
#install.packages("openNLP")
library(tm)
library(qdap)
require(openNLP)

c <- Corpus(DirSource("D:/CLASES/2021-I/Procesamiento de Lenguaje/Corpus-LDA/Corpus"))
summary(c)

#criar a matriz tf-idf
#dtm <- DocumentTermMatrix(c, control=list(wordLengths=c(3,Inf),weighting = weightTfIdf))
dtm <- DocumentTermMatrix(c)
x<-as.matrix(dtm)
rownames(x) <- paste(substring(rownames(x),1,5))

#distancia
m <- as.matrix(dist(x))
d <- as.dist(m)
stopifnot(d == dist(x))

#Clustering
#saving trace
write.csv(x,file="dtm-before-shorten-tf.csv")

#dendogram
groups <- hclust(d,method="ward.D")
plot(groups, hang=-1)
rect.hclust(groups,2)

#clustering
#k means algorithm, 2 clusters, 100 starting configurations
kfit <- kmeans(d, 4, nstart=100)
#plot – need library cluster
library(cluster)
clusplot(m, kfit$cluster, color=T, shade=T, labels=2, lines=0)


#find number of clusters
m.scaled<-scale(x)
k.max <- 15
data <- m.scaled
sil <- rep(0, k.max)

# Compute the average silhouette width for 
# k = 2 to k = 15
for(i in 2:k.max){
  km.res <- kmeans(data, centers = i, nstart = 25, iter.max=30)#https://stat.ethz.ch/pipermail/r-help/2006-March/102752.html
  ss <- silhouette(km.res$cluster, dist(data))
  sil[i] <- mean(ss[, 3])
}

# Plot the  average silhouette width
plot(1:k.max, sil, type = "b", pch = 19, 
     frame = FALSE, xlab = "Number of clusters k")
abline(v = which.max(sil), lty = 2)