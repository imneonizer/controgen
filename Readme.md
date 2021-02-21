## controgen

This is an IOT project to automatically `start / stop` ***custom power generator*** when mains goes off.

### Idea

Using vehicle engines from scrape and modifying them to act as low cost power generators. This is an engine based generator hence requires some level of automation to properly start the engine whenever mains power supply goes off, similarly switching it off again requires some additional precautions.

- Triggering self start switch for the engine
- Retrying multiple times of it fails to start
- Stopping the engine by pulling off levers

### OTA

This project supports over the air update to automatically update code base running on **NodeMCU**. Basically whenever the MCU restarts it looks for a familiar **ssid** to connect to for accessing internet once connected it can look for preloaded app url for updates and automatically pulls them.