# Motivation
This project aims to provide a "framework" that eases execution of tools in a loop. 

Sounds simple. And it is. But I needed hacky solutions during pentests, where a tool would just be perfect but could only perform a task for a single target (e.g. webapp endpoint, service, host: you name it). This project aims to simply add a "loop wrapper" with some helpers around such tools. 

So instead of writing your own hack from scratch, you'd just write a simple `main` function as in the `examples.py` utilizing the existing parsing, target filtering, logging, and execution classes/handlers as they fit. 

This way you can still get quick results while ensuring that these are consistent and everything gets logged. It could also save you from building target lists for each individual service, but work on one target file consistently (such as an nmap scan result) as you can precisely define on which targets your tool is executed.

In a perfect world, you could then use the hack you "built" to develop a new tool that optimizes a certain task once you have a little more time. This could be, for example, by adding a custom reporting handler that generates nice supporting material for a specific vulnerability. 

Please see:
* [examples.py](./examples.py)
* [DETAILS.md](./docs/DETAILS.md)
* [INTERFACES.md](./docs/INTERFACES.md)

