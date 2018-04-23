# Fuel Prices in the Netherlands

This project is about collecting the fuel prices around the Netherlands. An way of collecting this information is using the api that some companies like 'Makro' make publicly available.

## Using the project

For using this project I personally recommend using docker, I created an dockerhub repo for getting the latest version. [Docker hub](https://hub.docker.com/r/bartmachielsen/anwb-fuel-prices/)

Otherwise make sure to install *Python 3.6* with all the requiremenst from requirements.txt.

For connecting to the database the following environmental variables need to be set: (**IMPORTANT**)

- **MYSQL_HOST** (The location of the mysql server, port is default as 3306)
- **MYSQL_USER** (An mysql user with write and read permission)
- **MYSQL_PASSWORD** (Of the given user)
- **MYSQL_DATABASE** (The database needs to be already available, the structure will be automaticly created on the first run)

## About this project

### GOAL

The goal of this project is collecting data from all fuelstations in the Netherlands for mapping this data and maybe make something like predictions.

---

### PROBLEM

There are a lot of different fuelstations with different websites, for collecting this data a lot of webparsers need to be written. The other problem is with fuelstations that do not make their data publicly available.

---

### SOLUTION

For finding an solution to this problem i looked into different sources that already collect data about fuelprices, an large player in this field is the ANWB which has an app that supplies this data to anybody to find the cheapest station nearby.

___

#### ANWB

The 'ANWB' did already collect an wide range of sources. They written an range of parsers and also collect data by visits.

**Visits?**

Yeah, while taking an look at the data from the ANWB I noticed that some prices have an source that is been marked 'VISIT'.

**How does the ANWB know data from visits?**

The ANWB has an system that supplies discount to members who use their ANWB-creditcard for getting gas. [See this page for more information.](https://www.anwb.nl/auto/themas/tanken-met-ledenvoordeel)

The ANWB collects data from the bill from the creditcard in exchange for an discount. Not every fuelstation is an member on which you get discount. (there are around 3800 stations and anwb gives discount at 700)

But even if an fuelstation is not an member they still get used for getting the fuelprice (because the ANWB gets access to all fuelstation related creditcard transactions)

**How to use this data?**

The ANWB uses an REST API in their app for getting the latest collected fuelprice, this project uses that api for getting the stations and prices.

