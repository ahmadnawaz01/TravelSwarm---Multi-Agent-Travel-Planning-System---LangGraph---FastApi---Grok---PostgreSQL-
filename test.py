from tools.tavily_tool import tavily_search
from tools.flight_tool import search_flights

# res = tavily_search("best hotels in lahore?")
# print(res)


res=search_flights("Plan A 7 days trip to austria from pakistan")
print(res)