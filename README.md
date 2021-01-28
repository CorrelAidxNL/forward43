

# Forward43 by MasterPeace in collaboration with CorrelAid

**Forward43** is a data-driven project with the dream of supporting innovations worldwide by connecting them to decision-makers. We aim to create a match-making mechanism for decision-makers to better define their problems and connect them to ‘best-fit’ innovations through using semantic match-making, machine learning modules, and purposeful Artificial Intelligence.

The project aims to utilize vast data regarding innovations and find a smart framework to solve the world's most pressing issues facing societies, governments, organizations or businesses with current existing solutions.

**MasterPeace** is a grassroots peace-building organization that believes that the world is “7 billion talents, not issues” Therefore, we, in MasterPeace, use the soft-power of music, art, sports and play to mobilize and inspire young people.  We believe that there is more that we have in common than what separates us.

Therefore, we organize Dialogues within and between communities and stakeholders. We believe that the lack of perspective triggers polarization, extremism, and conflict. Therefore, we create perspective through capacity-building and leadership training for young people.

We offer a unique platform to a large community of changemakers, social entrepreneurs, volunteers, bloggers, journalists, musicians, entrepreneurs, and active citizens to connect and support each other by taking action.


**CorrelAid** is a non-partisan non-profit network of data science enthusiasts who want to change the world through data science. We dedicate our work to the social sector and those organizations that strive for making the world a better place. In order to improve data literacy in society, we share our knowledge within our network and beyond and are always looking for ways to broaden our horizons.

We value open knowledge management and transparency in our work wherever possible while complying with GDPR regulations and following strong principles of data ethics.

----------

## Project aim

Leading up to Forward43, MasterPeace found that their own database and the data available at other humanitarian, philatropic and entrepreneurial platforms offer relevant and in depth information on social innovations, which is often more valueble than the information found through conventional search engines (e.g. Google, Bing, Yahoo). Moreover, the teams involved became enthusiastic about gaining better insight into the landscape of social innovations. An overview of past and present projects enables social entrepreneurs to connect with like-minded people, build networks and learn from each other's experiences. Thus, in Forward43, we construct a search engine that enables MasterPeace chapters around the world to easily find and contact organisations and/or projects that have similar aims, operate in the same area, or have other relevant experience. 

---


## Project set-up


In order to build the search engine, we have created a pipeline to

 1.  Scrape social innovation data (Python)
 2. Automate periodic scraping (Docker)
 3. Collect the data in a database (Elasticsearch)
 4. Acces/search the database through dashboard/front end (Elasticsearch/...)


#### 1. Scrape social innovation data (Python) 
We collect data on social innovations and projects by scraping croudfunding and fundraising websites. Currently, we focus on the following sites:

- kickstarter.com
- ulule.com
- startsomegood.com
- justgiving.com (scraper upcoming)

On these sites, we collect the following information on projects:

- Title  
- Description  
- Status
- Innovation type (company, project)
- Country
- City
- Contact person/details
- Link
 
The data scraped is stored in JSON format so that it can be stored easily in the Elasticsearsch database (see step 3).


####  2. Automate periodic scraping (Docker)

To continuously serve its users and display the latest innovations, the engine should be regularly updated. We choose to automate this process with Docker.

#### 3. Collect the data in a database (Elasticsearch)

We use Elasticsearch to store and access the data. Elasticsearch is a distributed, free and open search and analytics engine for all types of data, stored in JSON format.

#### 4. Acces/search the database through dashboard/front end (Elasticsearch/...)

Elastisearch offers a data visualization and management tool for programmers called Kibana. However, since various users, non-programmers included, should be able to work with our search engine, we will build a more accessible user interface.

---