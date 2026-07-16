#!/usr/bin/env python3
"""A bank of original, relatable one-liner meme captions.

Written in-house (not scraped/reposted from Reddit, Instagram, etc.) so there's
no copyright or platform-ToS risk -- this sidesteps the same wall that blocked
Reddit's API. Organized by category so posts can rotate across moods/topics
instead of repeating the same flavor of joke back to back.

Dedup + rotation works the same way as the facts pipeline: text is tracked in
used_memes.json so nothing repeats until the whole bank has been used once.
"""

MEMES = {
    "work": [
        "Me: I'll start being productive after lunch.\nAlso me at 4:58pm: still haven't started.",
        "My job title should just be 'Professional Tab Switcher.'",
        "Nothing says 'I'm an adult' like getting excited about a good stapler.",
        "The meeting could've been an email. The email could've been silence.",
        "Monday me and Friday me are not the same species.",
        "I told my boss I work best under pressure. That's why I do everything at the last minute.",
        "'Quick call' is the biggest lie in the corporate dictionary.",
        "My productivity peaks exactly 12 minutes before the deadline.",
        "Coffee: because adulting requires a chemical head start.",
        "I've mastered the art of looking busy while thinking about lunch.",
    ],
    "adulting": [
        "Adulting is just googling how to do things while pretending you already know.",
        "Nobody warned me that 'being an adult' mostly means buying paper towels in bulk.",
        "I miss the days when my biggest responsibility was finishing my homework, not my life.",
        "Being an adult: cooking dinner and immediately wondering what to cook tomorrow.",
        "My 5-year plan is just 'survive the next 5 minutes' on repeat.",
        "Adulthood is realizing 8 hours of sleep is now a personality trait.",
        "I don't have a savings plan, I have a 'hope for the best' plan.",
        "The scariest words in adulthood: 'we need to talk about your car.'",
        "I peaked emotionally the day I found a parking spot right in front.",
        "Being a functional adult is 90% remembering where you put your keys.",
    ],
    "social_media": [
        "I don't have trust issues, I have 'why did they leave me on read' issues.",
        "My phone screen time report is basically a cry for help at this point.",
        "I opened the app to check one notification. That was 45 minutes ago.",
        "Nothing hits different like refreshing a page that has no new updates.",
        "My attention span has the battery life of a 2013 phone.",
        "I like my privacy the way I like my WiFi: strong and unshared.",
        "Online shopping cart: where dreams go to sit for three months untouched.",
        "I've rewatched the same 10 second video 6 times and learned nothing.",
        "My 'For You' page knows me better than my own family does.",
        "Double-tapping a post is the most commitment I've shown all week.",
    ],
    "food": [
        "'I'll just have a small snack' - the last words before I finish the whole bag.",
        "My relationship with the fridge is opening it every 20 minutes hoping something new appeared.",
        "Diet starts Monday. It's always Monday somewhere else.",
        "I don't skip leg day, I skip every day that isn't pizza day.",
        "Cooking for one is just an elaborate way of making dishes for yourself to wash.",
        "My cheat day has slowly become my cheat lifestyle.",
        "The gym is 10 minutes away. So is the couch. Guess which one won.",
        "I read the nutrition label after eating the whole thing, like a true optimist.",
        "Meal prepping is a beautiful lie I tell myself every Sunday.",
        "Water tastes better right after you've had literally anything else.",
    ],
    "weekend": [
        "Friday me makes plans that Saturday me immediately cancels.",
        "Sunday scaries hit different when Monday remembers everything you owe it.",
        "My weekend plan: nothing, and I'm already behind schedule.",
        "Weekends are just a 48-hour buffer between two Mondays.",
        "I spent the whole weekend recovering from a week I didn't even do that much in.",
        "Saturday plans: be productive. Saturday reality: rewatch a show for the third time.",
        "The weekend goes by faster than my patience during a Monday meeting.",
        "I don't wake up early on weekends, I wake up disappointed on weekdays.",
        "Sunday night is when your to-do list stages a surprise attack.",
        "Two-day weekends were clearly designed by someone who's never met a to-do list.",
    ],
    "relationships": [
        "Being single means never having to explain why you ate cereal for dinner.",
        "My love language is sending memes I think you'll relate to.",
        "Relationship status: in a committed relationship with my blanket.",
        "Nothing says romance like agreeing on what to watch without a 20 minute debate.",
        "I don't need a partner, I need someone to reach the top shelf.",
        "The real test of a relationship is sharing the last slice.",
        "'We should hang out soon' - a sentence that has ended more friendships than any argument.",
        "My idea of a perfect date is one where nobody talks and we just watch something.",
        "Texting 'lol' while not even smiling is basically a universal love language now.",
        "I fall in love with restaurants faster than I fall in love with people.",
    ],
    "introvert": [
        "Cancelled plans are the best plans.",
        "My social battery has a one-event limit per week.",
        "I don't ghost people, I just take really long social breaks.",
        "'Do you want to come out tonight?' is the scariest text I can receive.",
        "Home is where the WiFi automatically connects and nobody expects small talk.",
        "I've mastered the art of pretending I didn't see that text for three days.",
        "Small talk drains me faster than my phone battery on 1%.",
        "My favorite plan is the one that gets cancelled.",
        "I peaked socially the moment I said 'maybe' and meant 'no.'",
        "Introvert superpower: hearing my name called and immediately not responding.",
    ],
}

ALL_MEMES = [(category, text) for category, items in MEMES.items() for text in items]
