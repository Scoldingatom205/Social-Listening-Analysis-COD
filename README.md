# Project Overview
Call of Duty, a globally recognized franchise, garners immense feedback through various online platforms. 

This project aims to provide insights into player sentiment by collecting and analyzing reviews and comments from two key platforms: Steam and Reddit. The purpose of this project is to give the game's development team a clear understanding of the community's feedback, focusing on both positive and negative sentiment across critical areas like gameplay mechanics, map design, weapon balance, and server performance.

**Insights and Recommendations** are provided on the following key areas:
- **Sentiment Analysis:** How players feel about the game overall (positive, negative).
- **Topic Modeling:** Identifying key topics of discussion to prioritize development efforts.

My visualizations can be seen [here.](https://www.canva.com/design/DAGQnq2GjLA/VTC1VZbvmajNDR60eXSdnw/view?utm_content=DAGQnq2GjLA&utm_campaign=designshare&utm_medium=link&utm_source=editor)

The Python code used to collect data and perform quality checks can be found [here.](https://github.com/Scoldingatom205/Social-Listening-Analysis-COD/blob/main/scripts/extract_data.py)

The Python code used to [preprocess](https://github.com/Scoldingatom205/Social-Listening-Analysis-COD/blob/main/scripts/preprocess_data.py) then conduct sentiment analysis and topic modeling can be found [here.](https://github.com/Scoldingatom205/Social-Listening-Analysis-COD/blob/main/scripts/analysis.py)


# Dataset Structure
The data comprises user-generated feedback from Steam and Reddit. The datasets are processed for sentiment analysis, topic modeling, and manual clustering, ensuring a comprehensive understanding of the players’ feedback. We collected and analyzed over 6,000 player reviews, comments, and posts from Reddit and Steam.

All data was stored in MongoDB in BSON format for scalability and flexibility. 

![image](https://github.com/user-attachments/assets/922f3630-5107-46d9-a49e-84a398514df1)

The **data collection** for this analysis was carried out over two beta weekends:
- August 30 – September 4, 2024 (Beta Weekend One)
- September 6 – September 9, 2024 (Beta Weekend Two)
  
**But code is ready to automatically collect and analyze online posts after launch on October 25, 2024.**


# Executive Summary
### Overview of Findings
The collection of online posts, reviews, and comments across the two Call of Duty Black Ops 6 Beta Weekends reveals five main discussion clusters: Gameplay Experience, Weapon Balancing, Map Design, Server Performance, and Game/Engine Features. 

Huse **Spike in Conversations** after each largest surge in conversations occurred immediately after the launch of Beta Weekend 1, with discussions focusing primarily on gameplay (80% about new omni-movement) and game features (over 60% having trouble launching COD HQ). This trend steadies out throughout the weekend but picks up again after both weekends as players reflected on their experiences. **Weekend 2 Dominates** generating significantly more conversations than the first weekend. This is likely due to open access during the second weekend (as opposed to only pre-orders for Weekend 1), but also reflects Activision’s proactive engagement with the community. Quick responses to server issues, weapon balancing, and the addition of a new map kept players invested and engaged which is reflected on the sentiment graph below.

![image](https://github.com/user-attachments/assets/10582496-f26e-46d7-8d61-8df1a6b23afa)

### 1. Sentiment Analysis:
**Positive vs. Negative Sentiment:**

Players were generally positive, with Beta Weekend Two seeing an average of **60% increase in positive sentiment** compared to Beta Weekend One, despite having two fewer playable days.
- Positive Sentiment: Across the clusters, positive sentiment dominates, reflecting a generally optimistic or favorable outlook on the topics discussed. The majority of the positive feedback comes from clusters like **Gameplay Experience (56.6%)** suggesting people were enjoying the fast paceness, new omnimovement, skill base match making, and time to kill. 
- Negative Sentiment: Negative sentiment is most prominent in the **Map Design cluster (36.5%)**. This suggests that users are particularly critical of map structure, size, spawn points, and features around the map: head "glitches", favorable sides, breakable doors, glass, etc.

![image](https://github.com/user-attachments/assets/582cd8d0-939e-491e-b56a-d62cfdd533c5)


#### 2. Topic Modeling:
BERTopic, was used to identify and categorize the top topics mentioned in both Reddit posts and Steam reviews. Specific clsuters were manually made by my using my domain knowledge of the Call of Duty franchise and as a player of the Black Ops 6 beta. These topics reflect the most pressing concerns and highlights for players:

- **Game/Engine Features:** 'Cod HQ' (67.5%) and 'Emotes, Winner Circle, Body Shield' (32.6%) are the most talked-about features in this cluster. Cod HQ was the most talked about topic among players with the majority showing a dislike towards the game feature due to its complexity, long launch time, constant trouble shooting, and large file size.also feature prominently, pointing to frustrations with the game's technical stability, especially around restarting or launching issues.
- **Gameplay Experience:** **SBMM (Skill-Based Matchmaking) (57.1%)** is a major focus of player feedback, showing that players are particularly concerned with the fairness and balance of matchmaking with many complaining that their teammates are terrible or away-from-controller. **Movement (35.2%)** is another hot topic, highlighting how in-game mobility and responsiveness are vital aspects of the player experience most players expressing positive sentiment towards the new omnimovement. There is a bit of concern on the pace and hard-to-kill moveing players now. **Time-to-Kill (TTK) (7.7%**) rounds out the discussion, suggesting that the pace of gameplay and combat mechanics were a bit high which resuls in a lot of intensity of the game but difficult to survive.
- **Server Performance/Connectivity Issues:** A huge issue that called for two patch updates was server and connectivity issues. In addition to difficulty launching the game (cod hq), many players had issues with disconnection, laggy/skippy gameplay, and difficulty finding games at all.
- **Map Design:** Feedback was generally positive, with the two biggest concerns about maps being about Spawns (41.1%) and Small Map Size (38.7%). Players felt that spawns were not consistent and often too close to enemy lines causing an unfairness to the gameplay. A combination of fast movement, relatively high TTK, and small maps is an area of concern for many players as they feel the game is too hectic. Most players favoring for slightly bigger maps. The way game modes played on certain maps was not very unpleasant some players thought.
- **Weapon Balancing:** Players were calling for adjustments on the smgs as they felt they were overpowered. A lot of discussions had to do with good attachment combinations for these weapons as well as discourse over which are the best weapons on specific maps.


- **Commentary:** I clustered all not so important comments into one. Commentary consisted of comments regarding previous Call of Duty titles, criticism/compliments about Treyarch, Activision, and BO6, random talking points and references to other games. Not entirely relevant to our analysis but though I'd mention it.


### Importance for Treyarch, Activision
This analysis offers actionable insights that are crucial for Treyarch and Activision in optimizing the game and ensuring a successful launch. Key benefits include:

- **Enhancing Player Satisfaction and Retention:** By addressing issues with server performance, weapon balancing, and gameplay mechanics before launch, Treyarch can boost player satisfaction, encouraging long-term engagement and player retention.
- **Prioritizing Development Resources:** The analysis identifies the most critical areas for improvement, helping Treyarch allocate resources effectively. By focusing on gameplay, map design, and server performance, they can minimize post-launch fixes and enhance the overall player experience.
- **Boosting Launch Success and Managing Expectations:** The sentiment and topic analysis provides early warning signs for potential issues, allowing Treyarch to proactively address them before launch. Clear communication of fixes will help build community trust and set realistic player expectations.
- **Driving Community Engagement and Loyalty:** Quick responses to beta feedback, as demonstrated by the 9/8 patch, foster community loyalty. Maintaining this level of engagement will enhance player satisfaction and encourage positive word-of-mouth marketing.
- **Informed Business Decisions for Activision:** The insights gained from player feedback extend beyond gameplay, informing monetization strategies such as DLC, battle passes, and in-game purchases. Understanding player sentiment helps Activision align its in-game economy with what players want, improving revenue streams.
- **Gaining a Competitive Advantage:** The FPS market is highly competitive, and by leveraging real-time feedback to deliver a more polished, player-focused experience, Treyarch and Activision can stand out against competitors. Addressing key concerns early enhances their competitive edge and builds a more loyal player base.

# Caveats and Assumptions
- Text data is not the easiest to handle, especially on social media, where there is a long of slang and noninformative comments so I had to omit about 2k comments from analysis.
- I made assumptions about some of the topics in these clusters based on a few dozen comments. So if I saw that a topic assigned by BERTopic had [map, small, 'map_name'] then I would make assumptions that she comments were about small map designs. It is difficult to parse through all that text data manually especially since code does not have domain knowledge.
- I omitted one huge 'Commentary' cluster which consisted of comments regarding previous Call of Duty titles, criticism/compliments about Treyarch, Activision, and BO6, random talking points and references to other games since it did not provide me valuable insights
