rm(list = ls(all = TRUE))

# load package
libraries = c("FKF","quantmod","ggplot2","rjson","car","magick","gganimate","hrbrthemes","gifski","dplyr","viridis",
              "ggplot2","rjson","car","magick","gganimate","plotly")
lapply(libraries, function(x) if (!(x %in% installed.packages())) {
  install.packages(x)
})
lapply(libraries, library, quietly = TRUE, character.only = TRUE)

# people can change the wdir, it is the address where you put the results
wdir = "C:/Users/xo3ox/Desktop/DEDA_Class_2022_410707007_Tzu-Ying"
setwd(wdir)
dir.create("Results")
save = paste0(wdir, '/', "Results/")

file = paste0(wdir,"/AAPL.csv") 
start = '2022-11-18'
end = '2015-11-19'


APPLE = read.csv(file = file, header = TRUE)
APPLE = as.data.frame(APPLE)
APPLE = APPLE[which(APPLE$date <= start),]
APPLE = APPLE[which(APPLE$date >= end),]
count = nrow(APPLE)
price = APPLE$price
return = c(0, diff(log(APPLE$price))) #observations

#Allocate space:
xhat = rep(0,count) #a posteri estimate at each step
P = rep(0,count)  #a posteri error estimate
xhatminus=rep(0,count) #a priori estimate
Pminus=rep(0,count) #a priori error estimate
K=rep(0,count) #gain

#initialise guesses: assume true_value=0, error is 1.0
xhat[1] <- return[1] 
P[1] <- 1
Q_Select = c(0.03) # could change to a range
#estimate of measurement variance
R = 0.03
for (Q in Q_Select){ 
  for (k in 2:count){
    #time update
    xhatminus[k] <- xhat[k-1]
    Pminus[k] <- P[k-1] + Q
    
    #measurement update
    K[k] = Pminus[k] / (Pminus[k] + R)
    xhat[k] = xhatminus[k] + K[k] * (return[k] - xhatminus[k])
    P[k] = (1-K[k]) * Pminus[k]
  }
  
  png(paste0(save,'Return of APPLE- observable & predicted returns.png'),width=600,height=600,units="px",bg = "transparent")
  
  x= as.Date(APPLE$date)
  plot(x,return,col="blue",type="l",xlab = "Date",ylab ="Return",lwd = 1.5,cex.axis=1.5,cex.lab=1.5,cex.main=1.5)
  lines(x,xhatminus, col = "red",type="l",lwd = 1.5)
  legend(x = "topright", legend=c("Predict return", "Actual return"),
         col=c("blue", "red"), lty=1:2, cex=0.8)
  dev.off()
}

# movie of parameter interactions
gif_plot = data.frame(date = APPLE$date, xhatminus = xhatminus, return = return)
gif1 <-  gif_plot %>% 
  ggplot(aes(x=xhatminus, y=return))  +
  geom_line(colour = 'grey') +
  geom_point() +
  theme_ipsum() +
  theme(panel.background = element_rect(fill = "transparent", colour = NA), 
        panel.grid.major = element_blank(), 
        panel.grid.minor = element_blank(), 
        axis.line = element_line(colour = "black")) +
  transition_reveal(as.Date(date)) +
  ggtitle("Date: {frame_along}")

#save .gif
animate(gif1, renderer = gifski_renderer(paste0(save,'Observable return vs Predicted return.gif')), bg = "transparent",
        nframes = 100)

# MSE of different combination of Q and R
Q_Select = seq(from=0, to=0.03, by=0.0001)# could change to a range 0.001
#estimate of measurement variance
R_Select = seq(from=0, to=0.03, by=0.0001)

Result = matrix(nrow = length(Q_Select),ncol =length(R_Select))
for (i in 1 : length(Q_Select)){ #row number
  timestart<-Sys.time()
  for (j in 1 : length(R_Select)){ #Column number
    Q = Q_Select[i]
    R = R_Select[j]
    xhat = rep(0,count) #a posteri estimate at each step
    P = rep(0,count)  #a posteri error estimate
    xhatminus=rep(0,count) #a priori estimate
    Pminus=rep(0,count) #a priori error estimate
    K=rep(0,count) #gain
    
    #initialise guesses: assume true_value=0, error is 1.0
    xhat[1] <- return[1] 
    P[1] <- 1
    
    for (k in 2:count){
      #time update
      xhatminus[k] <- xhat[k-1]
      Pminus[k] <- P[k-1] + Q
      
      #measurement update
      K[k] = Pminus[k] / (Pminus[k] + R)
      xhat[k] = xhatminus[k] + K[k] * (return[k] - xhatminus[k])
      P[k] = (1-K[k]) * Pminus[k]
    }
    Result[i,j] = mean((return - xhatminus)^2)
  }
  timeend<-Sys.time()
  runningtime<-timeend-timestart
  print(paste0(timeend, " runing ", runningtime," finish ", as.character(Q)))
}

plot_Result = list(Q = Q_Select, R = R_Select, MSE= Result)
p <- plot_ly(x = plot_Result$Q, y = plot_Result$R, z = plot_Result$MSE)
# add_heatmap(p)
add_contour(p)


