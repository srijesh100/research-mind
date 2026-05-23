from agents import build_search_agent,build_reader_agent,writer_chain,critic_chain

def run_research_pipeline(topic:str)->dict:
    state={}

    #search agent working
    print("\n"+"="*50)
    print("step 1 -search agent is working")
    print("="*50)

    search_agent=build_search_agent()
    search_result=search_agent.invoke({
        "messages":[("user",f"find recent, reliable and detailed information about :{topic}")]
    })
    state["search_result"]=search_result["messages"][-1].content
    print(f"\nsearch result:{state["search_result"]}")

    #step 2 reader agent
    #search agent working
    print("\n"+"="*50)
    print("step 2 -reader agent is scraping top resources")
    print("="*50)

    reader_agent=build_reader_agent()
    reader_result=reader_agent.invoke({
        "messages":[("user",f"""
Based on the following search results about '{topic}
pick the most relevant URL and scrape it for deeper content.\n\n
search result:\n{state["search_result"][:800]}
""")]
    })
    state["scraped_content"]=reader_result["messages"][-1].content
    print(f"\nscrapped content:{state['scraped_content']}")

    #step 3

    print("\n"+"="*50)
    print("step 3 -writer is drafting the report")
    print("="*50)

    research_combined=(
        f"Search Result : \n {state['search_result']}\n\n",
        f"Detailed Scraped Content: \n {state['scraped_content']}\n\n"
    )

    state["report"]=writer_chain.invoke({
        "topic":topic,
        "research":research_combined
    })

    # step 4
    print("\n"+"="*50)
    print("="*50)
    print(f"\nstep 4 -final report :{state['report']} ")
    state["feedback"]=critic_chain.invoke({
        "report":state["report"]
    })
    print(f"\n Critic Report:\n{state['feedback']}")

    return state

if __name__=="__main__":
    topic=input("Enter your Research topic: ")
    run_research_pipeline(topic)
