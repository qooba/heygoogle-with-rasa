#### This file contains tests to evaluate that your bot behaves as expected.
#### If you want to learn more, please see the docs: https://rasa.com/docs/rasa/user-guide/testing-your-assistant/

## happy path 1
* greet: cześć !
  - utter_greet
* mood_great: cudownie
  - utter_happy

## happy path 2
* greet: siemano !
  - utter_greet
* mood_great: wspaniale
  - utter_happy
* goodbye: pa pa !
  - utter_goodbye

## sad path 1
* greet: hello
  - utter_greet
* mood_unhappy: źle
  - utter_cheer_up
  - utter_did_that_help
* affirm: tak
  - utter_happy

## sad path 2
* greet: cześć
  - utter_greet
* mood_unhappy: nie dobrze
  - utter_cheer_up
  - utter_did_that_help
* deny: nie
  - utter_goodbye

## sad path 3
* greet: cześć
  - utter_greet
* mood_unhappy: okropnie
  - utter_cheer_up
  - utter_did_that_help
* deny: nie
  - utter_goodbye

## say goodbye
* goodbye: pa pa!
  - utter_goodbye

## bot challenge
* bot_challenge: jesteś botem ?
  - utter_iamabot
