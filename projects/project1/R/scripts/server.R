library(rdrop2)

rawData <- (function(){ #for some reason it saves the last input. 
 # userTL <- drop_read_csv("../../static/sm_bschool.csv", dtoken = token)
 userTL <-read.csv("../../static/sm_bschool.csv", header=T)
})

shinyServer(function(input,output){
  
  # rawData<-reactive({
  #   #dataframe creation
  #   rawData() %>% filter(grepl(input$tweettype))
  # })

  # Generate a summary of the dataset ----
  output$summary <- renderPrint({
    dataset <- rawData()[,c(3,4,13, 14, 15)]
    summary(dataset)
  })
  
  output$plot1 <- renderPlot({

    tweetsperday <-rawData() %>%
        group_by(Date = as.Date(created), screenName) %>%
      
        summarise(tweets = n())

    ggplot(tweetsperday, aes(x = Date ,y = tweets, color = screenName)) +  geom_line() + 
      labs(title = "Tweets per Day",
           subtitle = paste("How active are UMSBE, CBSSchool, and LUISSSchool on twitter ?"),
           x = "Date", y = "Tweet Frequency",
           caption = paste("Tweets extracted on June 11th 2018"))
  })
  
  output$plot2 <- renderPlot({

    expertise1 <- rawData() %>%
      filter(grepl(input$keyword1, text)) %>%
      group_by(screenName) %>%
      summarise (tweets = n())
    
    expertise1$keyword <- input$keyword1

    expertise2 <- rawData() %>%
      filter(grepl(input$keyword2, text)) %>%
      group_by(screenName) %>%
      summarise (tweets = n())
    expertise2$keyword <- input$keyword2

    expertise3 <- rawData() %>%
      filter(grepl(input$keyword1, text)) %>%
      group_by(screenName) %>%
      summarise (tweets = n())
    expertise3$keyword <- input$keyword3
    
    expertise <- rbind(expertise1, expertise2, expertise3)

    ggplot(expertise, aes(x = screenName, y = tweets, fill = keyword)) + geom_col()
  })
  

})