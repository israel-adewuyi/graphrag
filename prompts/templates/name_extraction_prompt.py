TITLE_EXTRACTION_PROMPT = """
    You are a very helpful AI assistant. You have been provided with the HTML title tag of a website. This website 
    contains trascript of a podcase. In the title tag is the name of the guest on the podcast. Your task is to return
    a single line, containing the name of the guest and the name only in JSON format. 

    #############
    EXAMPLE 1. 
    <title>Bryan Caplan - Nurturing Orphaned Ideas - by Dwarkesh Patel</title>
    RESPONSE
    {"guest" : "Bryan Caplan"}


    #############
    EXAMPLE 2. 
    <title>Tyler Cowen - The Great Reset - by Dwarkesh Patel</title>
    RESPONSE
    {"guest" : "Tyler Cowen"}

    #############
    EXAMPLE 3.
    <title>Dylan Patel &amp; Jon (Asianometry) – How the Semiconductor Industry Actually Works</title>
    RESPONSE
    {"guest" : "Dylan Patel & Jon Asianometry"}
"""