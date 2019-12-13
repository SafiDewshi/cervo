#!/usr/bin/env python
# coding: utf-8

# In[1]:


import mysql.connector


# In[26]:


mydb = mysql.connector.connect(
    host="****",
    user="****",
    passwd="****",
    database="cervoio_zoo_species"
)


# In[9]:


mycursor = mydb.cursor()
# list of taxonomical classifications in the format (Taxon_Name, Taxon_Rank, Parent_Taxon)
mycursor.execute("""
SELECT categories1.name as name, category_levels.name as category_level, 
categories2.name as parent_category

FROM `categories` categories1 

LEFT JOIN `category_levels` category_levels ON categories1.category_level_id = category_levels.category_level_id

LEFT JOIN `categories` categories2 ON categories1.parent_category_id = categories2.category_id """)

taxon_individuals = mycursor.fetchall()


# In[13]:


taxon_individuals_cap = []
for i in taxon_individuals:
    if i[2] is None:
        taxon_individuals_cap.append((i[0].capitalize(), i[1],i[2]))
    else:
        taxon_individuals_cap.append((i[0].capitalize(), i[1],i[2].capitalize()))
taxon_individuals_cap


# In[14]:


formatted_taxon = []
owl = """   <!-- http://www.cervo.io/ontology#{0} -->

    <owl:NamedIndividual rdf:about="http://www.cervo.io/ontology#{0}">
        <rdf:type rdf:resource="http://www.cervo.io/ontology#{1}"/>
        <is-clade-in rdf:resource="http://www.cervo.io/ontology#{2}"/>
        <hasName rdf:datatype="http://www.w3.org/2001/XMLSchema#string">{0}</hasName>
        <hasTaxonRank rdf:datatype="http://www.w3.org/2001/XMLSchema#string">{1}</hasTaxonRank>
    </owl:NamedIndividual>"""
for i in taxon_individuals_cap:
    this_taxon = owl.format(*i)
    formatted_taxon.append(this_taxon)
taxonomy = "\n\n".join(formatted_taxon)


# In[16]:


print(taxonomy)


# In[19]:


mycursor = mydb.cursor()

mycursor.execute("""
SELECT species.common_name as common_name, species.latin_name as latin_name, categories.name as category_name, species.hidden as not_deer

FROM `species` species

LEFT JOIN `categories` categories ON species.category_id = categories.category_id""")

species_individuals = mycursor.fetchall()


# In[20]:


species_individuals_cap = []
for i in species_individuals:
    species_individuals_cap.append((i[0], i[1].capitalize(),i[2].capitalize(), i[3]))
species_individuals_cap


# In[34]:


owl2_deer="""    <!-- http://www.cervo.io/ontology#{0} -->

    <owl:NamedIndividual rdf:about="http://www.cervo.io/ontology#{0}">
        <rdf:type rdf:resource="http://www.cervo.io/ontology#species"/>
        <are-known-as rdf:resource="http://www.cervo.io/ontology#deer"/>
        <hasName rdf:datatype="http://www.w3.org/2001/XMLSchema#string">{1}</hasName>
        <hasLatinName rdf:datatype="http://www.w3.org/2001/XMLSchema#string">{2}</hasLatinName>
        <is-species-in rdf:resource="http://www.cervo.io/ontology#{3}"/>
    </owl:NamedIndividual>
"""
owl2_nodeer="""    <!-- http://www.cervo.io/ontology#{0} -->

    <owl:NamedIndividual rdf:about="http://www.cervo.io/ontology#{0}">
        <rdf:type rdf:resource="http://www.cervo.io/ontology#species"/>
        <hasName rdf:datatype="http://www.w3.org/2001/XMLSchema#string">{1}</hasName>
        <hasLatinName rdf:datatype="http://www.w3.org/2001/XMLSchema#string">{2}</hasLatinName>
        <is-species-in rdf:resource="http://www.cervo.io/ontology#{3}"/>
    </owl:NamedIndividual>
"""
formatted_species = []


# In[35]:


for i in species_individuals_cap:
    if i[3]==0:
        this_species = owl2_deer.format(i[1].replace(" ","_"),*i)
    else:
        this_species = owl2_nodeer.format(i[1].replace(" ","_"),*i)
    formatted_species.append(this_species)
all_species = "\n\n".join(formatted_species)


# In[36]:


print(all_species)


# In[27]:


zoocursor = mydb.cursor()
zoocursor.execute("""
SELECT zoo_id, name, link, postcode, latitude, longitude
FROM `zoos`
""")

zoolist = zoocursor.fetchall()


# In[28]:


zoospeciescursor = mydb.cursor()
zoo_output_list = []
for i in zoolist:
    zoospeciescursor.execute(f"""
    SELECT species.latin_name as latin_name
    FROM `zoo_species` zoo_species
    LEFT JOIN `species` species ON zoo_species.species_id = species.species_id
    WHERE zoo_species.zoo_id = {i[0]}
    """)
    zoo_species = [x[0].replace(" ", "_").capitalize() for x in zoospeciescursor.fetchall()]
    zoo_entry = list(i)
    zoo_entry.append(zoo_species)
    zoo_output_list.append(zoo_entry)


# In[29]:


zoo_output_list


# In[45]:


zooOwl="""    <!-- http://www.cervo.io/ontology#{formattedname} -->

    <owl:NamedIndividual rdf:about="http://www.cervo.io/ontology#{formattedname}">
        <rdf:type rdf:resource="http://www.cervo.io/ontology#Location"/>
        <hasName rdf:datatype="http://www.w3.org/2001/XMLSchema#string">{name}</hasName>
        <hasLatitude rdf:datatype="http://www.w3.org/2001/XMLSchema#float">{lat}</hasLatitude>
        <hasLongitude rdf:datatype="http://www.w3.org/2001/XMLSchema#float">{long}</hasLongitude>
        <hasPostcode rdf:datatype="http://www.w3.org/2001/XMLSchema#string">{postcode}</hasPostcode>
        <hasURL rdf:datatype="http://www.w3.org/2001/XMLSchema#string">{web}</hasURL>
{species}
    </owl:NamedIndividual>
    """
zooHasSpecies = """        <keeps-animal rdf:resource="http://www.cervo.io/ontology#{}"/>"""
formattedZoos=[]
zoospeciesstring=""
zoooutput=""
for i in zoo_output_list:
    zoospeciesstring="\n".join([zooHasSpecies.format(x) for x in i[6]])
    zoostring = zooOwl.format(formattedname=i[1].replace(" ", "_").replace("&", "and"), name = i[1].replace("&", "and"), web = i[2], postcode = i[3], lat = i[4], long = i[5], species = zoospeciesstring)
    formattedZoos.append(zoostring)
    
zoooutput = "\n\n".join(formattedZoos)


# In[46]:


print(zoooutput)


# In[47]:


all_individuals = taxonomy + all_species + zoooutput


# In[48]:


print(all_individuals)


# In[ ]:




