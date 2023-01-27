# AliceBot v0.9

Bot is still in an early stage of development 
more content will be added in the future

made by Nergan

## Contents

- [Description](#description)
- [Commands](#commands)
- [Game](#game)

## Description

Alice is a simple bot capable of rolling dices. Work is still in progress
more functionality can be added in the future per request.

Alice reacts on commands starting with "!" symbol. For more info
on how to use the commands read *Commands* section.

## Commands


### No category

These commands are available in any channel at any point of time

| **Command**     | **Description**                                                                                                                    | **Example**      |
|:----------------|:-----------------------------------------------------------------------------------------------------------------------------------|:-----------------|
| help <optional> | Will display a help menu listing all of the available commands. </br> As optional argument you can pass a name of command category | !help Dice rolls |


### RolePlay specific

These commands are limited to channels included in RolePlay category.
You won't be able to use them outside of this category.

| **Command** | **Description**                                                                                              | **Example** |
|:------------|:-------------------------------------------------------------------------------------------------------------|:------------|
| roll        | Alice will roll dices for you. First value is number of dices and second is number of sides on the dices     | !roll 2d20  |
| start_game  | Now you can start a simple dice game. This command used to launch th e game and finish stage to add players. | !start_game |
| connect     | Connects a player to the game. Will keep track of his progress                                               | !connect    |
| bet         | Rolls 1d6 and predicts the outcome of your bet                                                               | !bet 10     |
| get_height  | Displays current height of all players                                                                       | !get_height |


## Game

### Description

It's a simple dice game where the goal it to reach score 5000 or to remain the only one with the score more than 1.

### Rules

You can make your bet. Bet shouldn't be more than your current score.
Once you use *bet* command Alice will roll 1d6.
Result of your bet will be as following:

- **1**: Everyone losses. Especially the one who rolled the dice. You lose your total bet, other half of your bet
- **2/4**: You gain your bet
- **3/5**: You lose your bet and others will gain that score
- **6**: You gain double the amount

### How to play

1) Run *start_game* command
2) Everyone who wants to participate should use *connect* command
3) After everyone who wanted used *connect* type *start_game* again
4) Make bets and see who will win