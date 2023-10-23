from flask import Flask, request
import json
import logging
from math import floor

logging.basicConfig(filename='log_error.log', level=logging.ERROR)
app = Flask("productionplan")

@app.route("/productionplan", methods=['GET'])
def get(): #dummy get request
    return 'Hello'

@app.route("/productionplan", methods=['POST'])
def post():
    data = request.get_json()
    payload = Payload(data, co2_emitted_per_MWh=0.3)
    answer = payload.compute_answer()
    return answer

class Payload():
    def __init__(self, data, co2_emitted_per_MWh=0.3):
        self.load = data['load']
        self.fuels = data['fuels']
        self.powerplants = [] #this list will be sorted
        self.sum_pmax = 0

        #retrieving and computing powerplants informations
        for powerplant in data['powerplants']:
            powerplant['p'] = 0.0
            if(powerplant['type'] == 'gasfired'):
                powerplant['cost_per_MWh'] = self.fuels['gas(euro/MWh)']/powerplant['efficiency'] + self.fuels['co2(euro/ton)']*co2_emitted_per_MWh
            if(powerplant['type'] == 'turbojet'):
                powerplant['cost_per_MWh'] = self.fuels['kerosine(euro/MWh)']/powerplant['efficiency']
            if(powerplant['type'] == 'windturbine'):
                powerplant['cost_per_MWh'] = 0
                powerplant['pmax'] = floor(powerplant['pmax']*self.fuels['wind(%)']/100 *10) / 10 #updating pmax wrt the wind%. floor to one decimal
            self.powerplants.append(powerplant)

        self.powerplants.sort(key=lambda k: (k['cost_per_MWh'], k['pmax']))

    def compute_answer(self):
        remaining = self.load
        for i in range(len(self.powerplants)):
            powerplant = self.powerplants[i]
            pmax = powerplant['pmax']
            pmin = powerplant['pmin']

            if not remaining:
                break

            #case where pmax <= remaining
            if pmax <= remaining:
                powerplant['p'] = pmax
                remaining -= pmax

            #case where pmin <= remaining < pmax then p=remaining and the answer is done
            elif pmin <= remaining:
                powerplant['p'] = remaining
                break

            #case where remaining < pmin then p = pmin and the surplus (pmin-remaining) is subtracted from the previous powerplants
            else:
                powerplant['p'] = pmin
                surplus = pmin - remaining
                for j in range(i-1, -1, -1):
                    previous_pmin = self.powerplants[j]['pmin']
                    previous_p = self.powerplants[j]['p']
                    updated_previous_p = previous_p - surplus
                    
                    #the updated p still has to respect the pmin condition
                    if updated_previous_p >= previous_pmin:
                        self.powerplants[j]['p'] = updated_previous_p
                        surplus = 0
                        break
                    else:
                        self.powerplants[j]['p'] = previous_pmin
                        surplus += previous_pmin - previous_p

                #no optimized answer for now if there is still a surplus at the first plant, we proceed to the next plant in the loop
                remaining = surplus

        #writing the answer
        answer = [{"name": powerplant['name'], 'p': powerplant['p']} for powerplant in self.powerplants]
        return json.dumps(answer, indent=4)

if __name__ == '__main__':
    app.run(debug=True, port=8888)
