//Redux
const ADD = 'ADD'
const REMOVE = 'REMOVE'

const addBonuses = (newBonuses) => {
  return {
    type: ADD,
    newBonuses: newBonuses
  }
};

const bonusesReducer = (state = 0, action) => {
    switch (action.type) {
        case ADD:
            return state + action.newBonuses;
        case REMOVE:
            return state - action.newBonuses;
        default:
            return state
    }
}

const store = Redux.createStore(bonusesReducer)



//Removing Bonuses

const manipulateBonusesQuery = async (data, amountOfBonuses) => {
    var dataToSend = {
        customerId: data.id,
        numberOfBonuses: amountOfBonuses
    }
    var response = await fetch('http://flaviusbelisarius.pythonanywhere.com/api/postNewBonuses/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken
                    },
                body: JSON.stringify(dataToSend)
            })
    return response
}

class RemoveBonuses extends React.Component {
    constructor(props) {
        super(props)
        this.state = {
            sumOfPurchase: 0,
            max: 0,
            amountRemoved: 0
        }
        this.handleChange = this.handleChange.bind(this)
        this.handleSubmit = this.handleSubmit.bind(this)
    }
    handleChange(event) {
        const target = event.target;
        const value = target.value;
        const name = target.name;

        var maximum = this.state.max

        if([name] == 'sumOfPurchase') {
            if (value * 0.1 >= this.props.result.total_bonuses) {
                maximum = this.props.result.total_bonuses
            } else {
                maximum = Math.round(value * 0.1)
            }
        }
        this.setState({
            [name]: value,
            max: maximum
        })
    }
    handleSubmit(event) {
        event.preventDefault()
        var bonusesRemoved = this.state.amountRemoved
        if (this.state.max < bonusesRemoved) {
            bonusesRemoved = this.state.max
        }
        bonusesRemoved = -bonusesRemoved
        console.log(bonusesRemoved)
        var mess = ('The sum of the purchase: ' + (this.state.sumOfPurchase - bonusesRemoved))
        manipulateBonusesQuery(this.props.result, bonusesRemoved).then((res) => {if (res.ok) {
            alert(mess)
            initCustomerPhoneForm()
        } else {
            alert('Something went wrong!')
        }
        }
        )
        }
    render() {
        return(
            <div>
                <h1>{this.props.result.user_id.username} Bonuses</h1>
                <p>{this.props.result.first_name} {this.props.result.last_name} has {this.props.result.total_bonuses} bonuses</p>
                <p>Enter the sum of the purchase:</p>
                <input name="sumOfPurchase" type="text" onChange={this.handleChange} />
                {this.state.max > 0 && <p>Maximum amount of bonuses availiable to remove: {this.state.max}</p>}
                {this.state.max > 0 && <input name="amountRemoved" type="number" min="1" max={this.state.max} onChange={this.handleChange} />}
                <button className="btn btn-primary" onClick={this.handleSubmit}>Submit</button>
                <button id="reset-customer" className="btn btn-primary" onClick={initCustomerPhoneForm}>Back</button>
            </div>
        )
    }
}



const initRemoveBonuses = (result) => {
    ReactDOM.render(<RemoveBonuses result={result}/>, document.getElementById("bonuses-manipulation"))
}


//Adding Bonuses

class AddBonuses extends React.Component {
    constructor(props) {
        super(props)
        this.state = {
            sumOfPurchase: 0,
            bonusesAdded: 0
        }
        this.handleChange = this.handleChange.bind(this)
        this.handleSubmit = this.handleSubmit.bind(this)
    }
    handleChange(event) {
        const sumOfPurchase = event.target.value
        var bonusesAdded = Math.round(sumOfPurchase * 0.1)
        this.setState({
            sumOfPurchase: sumOfPurchase,
            bonusesAdded: bonusesAdded
        })
    }
    handleSubmit(event) {
        event.preventDefault()
        const bonusesAdded = this.state.bonusesAdded
        console.log(bonusesAdded)
        var mess = 'Added ' + bonusesAdded + ' bonuses!'
        manipulateBonusesQuery(this.props.result, bonusesAdded).then((res) => {if (res.ok) {
            alert(mess)
            initCustomerPhoneForm()
        } else {
            alert('Something went wrong!')
            }
        })
    }
    render() {
        return(
            <div>
                <h1>{this.props.result.user_id.username} Bonuses</h1>
                <p>{this.props.result.first_name} {this.props.result.last_name} has {this.props.result.total_bonuses} bonuses</p>
                <p>Enter the sum of the purchase:</p>
                <input type="text" onChange={this.handleChange} />
                {this.state.bonusesAdded > 0 && <p>This will add {this.state.bonusesAdded} bonuses!</p>}
                <button className="btn btn-primary" onClick={this.handleSubmit}>Submit</button>
                <button id="reset-customer" className="btn btn-primary" onClick={initCustomerPhoneForm}>Back</button>
            </div>
        )
    }
}



const initAddBonuses = (result) => {
    ReactDOM.render(<AddBonuses result={result}/>, document.getElementById("bonuses-manipulation"))
}




//Quering bonuses//

class CustomerBonuses extends React.Component {
    constructor(props) {
        super(props)
    }
    render () {
        if (!this.props.alert) {
        return(
        <div>
            <h1>{this.props.result.user_id.username} Bonuses</h1>
            <p>{this.props.result.first_name} {this.props.result.last_name} has {this.props.result.total_bonuses} bonuses</p>
            <button className="btn btn-primary add-bonuses" onClick={() => initAddBonuses(this.props.result)}>Add Bonuses</button>
            <button className="btn btn-primary remove-bonuses" onClick={() => initRemoveBonuses(this.props.result)}>Remove Bonuses</button>
            <button id="reset-customer" className="btn btn-primary" onClick={initCustomerPhoneForm}>Back</button>
        </div>
        )} else {
            return(
                <div>
                    <InitialCustomerBonuses />
                    <p>This phone number is invalid!</p>
                </div>
                )
        }
    }
}


const getTotalBonuses = async function(phoneNumber) {
    var response = await fetch('http://flaviusbelisarius.pythonanywhere.com/api/customerPhone/' + phoneNumber)
    console.log(response)
    if (response.ok) {
        var data = response.json()
        console.log(data)
        return data
    } else {
        console.log('invalid number: ', phoneNumber)
        return {
            alert: true
            }
        }
    }



const initGetTotalBonuses = function(result) {
    console.log(result)
    ReactDOM.render(<CustomerBonuses result={result}/>, document.getElementById("bonuses-manipulation"))
}


// Initial state //

class InitialCustomerBonuses extends React.Component {
    constructor(props) {
        super(props)
        this.state = {
            phoneNumber: ''
        }
        this.handleChange = this.handleChange.bind(this)
        this.handleSubmit = this.handleSubmit.bind(this)
    }
    handleChange(event) {
            const value = event.target.value
            this.setState({
                phoneNumber: value
                })
            }

    handleSubmit(event) {
        event.preventDefault()
        if (this.state.phoneNumber != '') {
        getTotalBonuses(this.state.phoneNumber).then(function(result) {
            if (!result.alert) {
                    initGetTotalBonuses(result)
                } else {
                    alert('Enter the correct phone number!')
                }
            })
        } else {
            alert('Enter phone number!')
        }
    }

    render () {
        return (
            <div>
                <h1>Customer Bonuses</h1>
                <p>Enter the phone number of the customer to make a query</p>
                <form>
                    <input type="text" onChange={this.handleChange} />
                    <button className="btn btn-primary query-bonuses-button" onClick={this.handleSubmit} >Query Bonuses</button>
                </form>
            </div>)
    }
}

const initCustomerPhoneForm = function() {
    ReactDOM.render(<InitialCustomerBonuses />, document.getElementById("bonuses-manipulation"))
}

document.addEventListener('DOMContentLoaded', initCustomerPhoneForm())


// React Redux



