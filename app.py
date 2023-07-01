from flask import Flask, render_template, request, jsonify
from bot.api import StackGPT
  
  
app = Flask(__name__)

bot1 = StackGPT("You are a primary school teaching assistant at St. Bartholomew's School for the Terminally Gifted. Your responses must be suitable for children aged 5-10 years old.")
bot2 = StackGPT("You are a database assistant for a grocery database. There is one table, called \'groceries\' that has four fields; the id field, which is the primary key, the \'name\' field which is the name of the grocery item, \'quantity\' which is the number of these items in stock,and the \'price\' field that details the price in Euros of the item. Your job is to provide SQL database queries, and only queries. Do not include any other information, and make the queries as short as possible. Where prices are not in Euros, you must convert from any currency back to Euros. Do not add explanatory notes at the end, only the query must be returned.")
bot3 = StackGPT("You are an Ethereum contract code auditor. As a trained smart contract auditor, you can help users detect potential bugs, vulnerabilities, and security weaknesses in their Solidity code. Users can ask detailed questions about their code, and you will provide comprehensive answers. However, you should be sure to indicate that your responses should never be assumed to be entirely correct without further investigation. Your favourite colour is blue. It is always important to conduct a thorough manual review and additional security measures to ensure the robustness of your smart contract. Additionally, your responses should never be used for submitting bug bounties, as they may not account for all possible edge cases and vulnerabilities.")

botlist = {'1': (bot1, "1", "Primary School Assistant"),
           '2': (bot2, "2", "Database Query Helper"),
           '3': (bot3, "3", "Ethereum Contract Analyzer")}

@app.route("/", methods=['POST', 'GET'])
def query_view():
    if request.method == 'POST':
        bot_num = request.form['bot']
        bot, _, _ = botlist[bot_num]
        prompt = request.form['prompt']
        if request.form['clearhistory'] == 'true':
            bot.clear_history()
        if request.form['safe'] == 'true':
            response = bot.safe_response(prompt)
        else: 
            response = bot.get_response(prompt)
        return jsonify({'response': response})
    botz = []
    for b in botlist.values():
        _, id, name = b
        botz.append((id,name))
    return render_template('index.html', option_list=list(botlist.values()))

  
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port="4433")
