# Multiply Portfolio Tracker


## Goals of system
- Display total portolio value, cumulated from across all investment platforms (as of now: etoro, trading 212, wio)
    - Try to recreate what you would see on investment platform, but in 1 location for all platforms
-- Should then also be able to see classic breakdown per platform
- Subscribe to a websocket for an instrument, and display price feed


### Stretch Goals:
- be able to see if there is a cheaper place to invest at a certain point in time (due to spread + costs)


## Things to think about:
- Whilst managing rate limits, how can we get all the data we need to provide similar experience you would get on investment application
### On startup 
- should scrape all live trades


## Plan

On app startup:
- fetch trades for at least last 3 years


During running, at fixed rate of 5 mins (this is not concrete) fetch:
- historical trades from last week (to update if a trade is closed)
- open trades

Account equity could be fetched every 30 seconds possibly



