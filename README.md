# Treasure Hunting Game

This is two of the homework projects of my Contemporary Data Management Systems course. It is a really simple treasure hunting game. There are two directories in this repository and each contains one system. The two treasure hunting games are similar since they share the same game scenario. The major difference between these two versions is version 1 uses MongoDB and version 2 uses PostgreSQL.

In each directory, there is a report (markdown document) describes the design of the database, functions and tests. Most codes are written in Python, stores in TreasureHunt directory. There are 4 document collections (players, treasures, market and log) in version 1, and 4 tables (players, treasures, logs and logs_overflow) in version 2. 

-----

Here follows the description of the game.

Consider the following game scenario:

1. Each game player has a certain number of gold coins and treasures. There is a market where players can buy and sell treasures. Players can put treasures on the market and determine the price themselves. Other players can purchase treasures by paying enough gold coins.

2. Treasures are divided into two categories: one is tools, which determines the player's ability to work; the other is accessories, which determines the player's luck.

3. Each player can obtain a treasure through treasure hunting every day, and the value of the treasure is determined by the player's luck. Each player can earn gold coins through labor every day, and the amount earned is determined by the player's work ability. (A day in the game can be 1 minute, 5 minutes, or 10 minutes in real life. You can set it yourself.)

4. Each treasure has its own name (try not to repeat it). The treasures that each player can wear are limited (for example, a player can only wear one tool and two accessories). Excess treasure is placed in storage boxes, which have no function, but can be sold in the market.

5. Treasures listed on the market must be in the storage box and remain in the storage box until the treasure is sold. Listed treasures can be withdrawn and relisted at a new price. When the storage box cannot be loaded, the treasure with the lowest luck or work ability value will be automatically recovered by the system.

6. Assume that the game never stops and the player's ultimate goal is to obtain the best treasure.

Please build a hypothetical web game based on the above scenario, which can be played by multiple people online. The interface is as simple as possible. The background database uses mongodb/postgresql. The following operations are provided for game players: treasure hunting, making money, wearing treasures, browsing the market, buying treasures, listing treasures, and recovering treasures.
