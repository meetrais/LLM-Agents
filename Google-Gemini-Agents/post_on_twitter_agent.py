import os
import requests
from bs4 import BeautifulSoup
from google import genai

# --- API Keys (from environment variables) ---
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    print("ERROR: Google API Key not found. Set GOOGLE_API_KEY environment variable.")
    exit()

# --- Function Definitions (Tools for the Agents) ---

def search_google_news(query: str) -> list:
    """Searches Google News (Simplified Web Scraping)."""
    try:
        url = f"https://news.google.com/search?q={query}&hl=en-US&gl=US&ceid=US%3Aen"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")
        articles = []
        for item in soup.find_all("div", class_="SoaBEf"):
            title_element = item.find("h3", class_="ipQwMb")
            if title_element:
                title = title_element.text
                link_element = item.find('a', href=True)
                if link_element:
                    link = "https://news.google.com" + link_element['href'][1:]
                    articles.append({'title': title, 'link': link})
        return articles
    except requests.exceptions.RequestException as e:
        print(f"Error during Google News search: {e}")
        return []
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return []
    
def create_twitter_post(news_title: str, news_link: str) -> str:
    """
    Generates X/Twitter post content.  This is now a *function* to be used as a tool.
    """
    model = genai.GenerativeModel('gemini-1.5-pro-latest')
    prompt = (
        f"Create a short, engaging X/Twitter post about this news: '{news_title}'. "
        f"Link: {news_link} Keep it under 280 characters (including the link). "
        f"Include relevant hashtags. Be concise and attention-grabbing."
    )
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error during tweet generation: {e}")
        return ""

def check_inaccuracy(twitter_post: str, news_title: str) -> str:
  """Checks for inaccuracies (VERY BASIC - NEEDS IMPROVEMENT). Now a function."""
  keywords = news_title.lower().split()
  if any(keyword in twitter_post.lower() for keyword in keywords):
      return "No obvious inaccuracies detected (basic check)."
  else:
      return "Possible inaccuracy: Post might be missing key information."

def post_to_twitter(twitter_post: str) -> str:
    """Posts to X/Twitter (SIMULATED).  Now a function."""
    print(f"SIMULATED X/Twitter post: {twitter_post}")
    return "Post successful (simulated)"
    # ... (Uncomment and implement Tweepy as before) ...

# --- Tool Definitions (for Gemini) ---

tools = [
    {
        "function": {
            "name": "search_google_news",
            "description": "Searches Google News for the latest news on a given topic.",
            "parameters": {
                "type": "OBJECT",
                "properties": {
                    "query": {
                        "type": "STRING",
                        "description": "The search query.",
                    }
                },
                "required": ["query"],
            },
        }
    },
    {
        "function": {
            "name": "create_twitter_post",
            "description": "Generates X/Twitter post content based on news title and link.",
            "parameters": {
                "type": "OBJECT",
                "properties": {
                    "news_title": {
                        "type": "STRING",
                        "description": "The title of the news article.",
                    },
                    "news_link": {
                        "type": "STRING",
                        "description": "The link to the news article.",
                    },
                },
                "required": ["news_title", "news_link"],
            },
        }
    },
    {
        "function": {
            "name": "check_inaccuracy",
            "description": "Checks a Twitter post for potential inaccuracies against a news title.",
            "parameters": {
                "type": "OBJECT",
                "properties": {
                    "twitter_post": {
                        "type": "STRING",
                        "description": "The content of the Twitter post.",
                    },
                    "news_title": {
                        "type": "STRING",
                        "description": "The title of the original news article.",
                    },
                },
                "required": ["twitter_post", "news_title"],
            },
        }
    },
    {
        "function": { # DUMMY FUNCTION, REPLACE WITH TWEEPY INTEGRATION
            "name": "post_to_twitter",
            "description": "Posts the given content to X/Twitter.",
            "parameters": {
                "type": "OBJECT",
                "properties": {
                    "twitter_post": {
                        "type": "STRING",
                        "description": "The content of the Twitter post to publish.",
                    },
                },
                "required": ["twitter_post"],
            },
        }
    },
]

# --- Main Agent Logic (using Function Calling) ---

def run_agent_workflow():
    """Runs the multi-agent workflow using function calling."""
    model = genai.GenerativeModel(model_name='gemini-1.5-pro-latest', tools=tools)
    chat = model.start_chat()

    # Initial prompt to start the process
    initial_prompt = "Find the latest news about AI and post it on Twitter."
    response = chat.send_message(initial_prompt)

    # Process the conversation history, handling function calls
    while True: #loop through the conversation
        if response.candidates and response.candidates[0].content.parts:
            part = response.candidates[0].content.parts[0]
            if part.function_call:
                function_call = part.function_call
                function_name = function_call.name
                function_args = function_call.args

                print(f"Calling function: {function_name} with args: {function_args}")

                if function_name == "search_google_news":
                    results = search_google_news(**function_args)  # Call the function
                    if results:
                      #Select top result
                      top_result = results[0]
                      chat.send_message(
                          genai.Content(
                              parts=[
                                  genai.Part(text=f"Here are the news items I found: {top_result}"),
                              ],
                              role="model",
                          )
                      )

                      #Now, ask gemini to create post
                      response = chat.send_message(f"Create a twitter post for this news item, title:{top_result['title']}, link: {top_result['link']}")

                    else:
                      response = chat.send_message("Could not find any news items") #continue #if no news found

                elif function_name == "create_twitter_post":
                    # Extract arguments and call the function
                    news_title = function_args.get("news_title")
                    news_link = function_args.get("news_link")
                    if news_title and news_link:
                        tweet_content = create_twitter_post(news_title, news_link)
                        # Send the tweet content back to the model as a function response
                        chat.send_message(
                            genai.Content(
                                parts=[
                                    genai.Part(text=f"Here's the generated tweet: {tweet_content}"),
                                ],
                                role="model",
                            )
                        )
                        # check for inaccuracies
                        response = chat.send_message(f"Check the following tweet for inaccuracies.  Tweet content: {tweet_content}, news title: {news_title}")
                    else:
                        response = chat.send_message("Missing news title or link for tweet creation.")

                elif function_name == "check_inaccuracy":
                    twitter_post = function_args.get("twitter_post")
                    news_title = function_args.get("news_title")
                    if twitter_post and news_title:
                        inaccuracy_result = check_inaccuracy(twitter_post, news_title)

                        chat.send_message(
                            genai.Content(
                                parts=[
                                    genai.Part(text=f"Inaccuracy check result: {inaccuracy_result}"),
                                ],
                                role="model",
                            )
                        )

                        # Post if no inaccuracy is detected
                        if "inaccuracy" not in inaccuracy_result.lower():
                          response = chat.send_message(f"Post the following tweet to twitter: {twitter_post}")
                        else:
                            print("Post skipped due to potential inaccuracies.")
                            break #exit loop

                    else:
                        response = chat.send_message("Missing tweet or title for inaccuracy check")
                elif function_name == "post_to_twitter":
                    twitter_post = function_args.get("twitter_post")

                    if twitter_post:
                        post_result = post_to_twitter(twitter_post)  # Call your posting function
                        chat.send_message(
                            genai.Content(
                                parts=[
                                    genai.Part(text=f"Twitter post result: {post_result}"),
                                ],
                                role="model",
                            )
                        )
                        break #exit when posted
                    else:
                      response = chat.send_message("Missing tweet to post") #ask for the tweet
                else:
                    response = chat.send_message(f"Unknown function call: {function_name}") #handle unknown function call

            else: #no function was called.
                if response.text:
                  print(f"Model: {response.text}")  # Print the model's response
                  #if there is not text, then end the conversation.
                else:
                  print("No response text")
                break
        else: #no candidates returned
            print("No candidates returned")
            break #end loop

if __name__ == "__main__":
    run_agent_workflow()