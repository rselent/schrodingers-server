# Schrödinger's Server

## If a service is down, did you kill it?

When complete, Schrödinger's Server should be able to identify if a URL/service is up/down.

Short and sweet.

-----

### Min Viable Product:

- [ ] Build a service that allows a user to register and ping any number of URLs to see if the  
service is down
- [ ] Display a list of the services, as well as their current status

### Stretch Goals:

- [ ] Be able to Nest sub-services within a higher level one.  
  - For example: AWS has multiple regions each with their own status.  Slack has several  
  different systems, each with their own status:
    - [ ] chat, 
    - [ ] notifications, 
    - [ ] login, 
    - [ ] etc
- [ ] Create the ability to ping on a frequency and refresh automatically
- [ ] Combine multiple services into a high level “Is it Working” signal.  
  - For example: Slack + Email + Google => \<Business> is Alive
