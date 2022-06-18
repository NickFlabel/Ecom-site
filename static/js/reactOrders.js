console.log('reactOrders is loaded')

const makeOrderPaid = async function (id) {
    var put = async function(id) {
        var data = {
            id: id
        }
        var response = await fetch('http://flaviusbelisarius.pythonanywhere.com/api/order/acceptPayment/', {
            method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken
                    },
                body: JSON.stringify(data)
        })
        return response
    }
    const answer = window.confirm("Do you want to accept payment for this order?")
    if (answer) {
        put(id).then(function(result) {
        if (result.ok) {
            initAllOrders()
            alert('The order is paid!')
            orderInfo(id, true)
        } else {
            alert('Something went wrong!')
        }
    })
    }
}



const closeOrder = function (id) {
    var put = async function(id) {
        var data = {
            id: id
        }
        var response = await fetch('http://flaviusbelisarius.pythonanywhere.com/api/order/serveOrder/', {
            method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken
                    },
                body: JSON.stringify(data)
        })
        return response
    }
    const answer = window.confirm("Do you want to close this order?")
    if (answer) {
        put(id).then(function(result) {
            if (result.ok) {
                initAllOrders()
                alert('The order is served!')
                orderInfo(id, false)
            } else {
                alert('Something went wrong!')
        }
    })
    }
}

class EmptyButtons extends React.Component {
    constructor(props) {
        super(props)
    }
    render() {
        return(
            <div>
            </div>
            )
    }
}

class EmptySearch extends React.Component {
    constructor(props) {
        super(props)
    }
    render() {
        return(
            <div>
            </div>
            )
    }
}

class BonusesSearch extends React.Component {
    constructor(props) {
        super(props)
        this.state = {
            inputPhone: '',
            inputNumber: '',
            message: ''
        }
        this.handleChange = this.handleChange.bind(this)
        this.handleSubmit = this.handleSubmit.bind(this)
    }
    handleChange (event) {
        const target = event.target;
        const value = target.value;
        const name = target.name;

        this.setState({
            [name]: value
        })
        this.setState({
            message: ''
        })
    }
    handleSubmit (event) {
        event.preventDefault()
        if (event.target.name == "searchPhone") {
            getOrdersByPhone(this.state.inputPhone).then(function(result) {
                if (result.id) {
                    ReactDOM.render(<PhoneNumberOrderList orders={result.order_set} />, document.getElementById('phone-order-list'))
                    initOrderButtons(true)
                } else {
                    alert('This phone number is invalid')
                }
            })
        } else {
            orderInfo(this.state.inputNumber, true)
        }
    }
    render () {
        return (
            <div>
                <h1>Order Search</h1>
                <h3>Phone Number Search</h3>
                <p>Enter the phone number of the Customer</p>
                <input name="inputPhone" type="text" onChange={this.handleChange} />
                <button name="searchPhone" className="btn btn-primary" onClick={this.handleSubmit}>Search by Phone Number</button>
                <h3>Order Number Search</h3>
                <p>Enter the number of the Order</p>
                <input name="inputNumber" type="text" onChange={this.handleChange} />
                <button name="searchNumber" className="btn btn-primary" onClick={this.handleSubmit}>Search by Order Number</button>
                {this.state.message && <p>{this.state.message}</p>}
                <div id="phone-order-list">
                </div>
            </div>
            )
    }
}

class PhoneNumberOrderList extends React.Component {
    constructor(props) {
        super(props)
    }
    render () {
            var allOrders = []
            for (let i = 0; i < this.props.orders.length; i++) {
                if(this.props.orders[i].complete && !this.props.orders[i].served) {
                    allOrders.push(<SingleOrder key={this.props.orders[i].id} id={this.props.orders[i].id} is_paid={this.props.orders[i].is_paid} served={this.props.orders[i].served} />)
                }
            }
        return (
            <div>
            <ol key="allOrders">
                {allOrders}
            </ol>
            <button onClick={clearSearch} className="btn btn-success">Clear all</button>
            </div>
            )
    }
}

class OrderManipulationButtons extends React.Component {
    constructor(props) {
        super(props)
    }
    render() {
        return(
            <div>
                {this.props.is_paid ? <button className="btn btn-primary" onClick={() => {closeOrder(this.props.id)}}>Close Order</button> :
                <button className="btn btn-primary" onClick={() => {makeOrderPaid(this.props.id)}}>Accept Payment</button>}
            </div>
            )
    }
}

class OrderItemSet extends React.Component {
        constructor(props) {
            super(props)
        }
        render () {
            return(
            <li key={this.props.item.product_id} >{this.props.item.product_id} - {this.props.item.quantity} items</li>
        )
        }
    }



class OrderItem extends React.Component {
        constructor(props) {
          super(props);
         }
        render() {
                let orderItems = []
                for (let i = 0; i < this.props.orderitem_set.length; i++) {
                    orderItems.push(<OrderItemSet key={this.props.orderitem_set[i].product_id} item={this.props.orderitem_set[i]} />)
                }
                let styles = {
                    width: "75%",
                    height: "50vh",
                    overflowY: "scroll"
                }
                const date = new Date(this.props.date_ordered)
                const formattedDate = date.toLocaleDateString("en-GB", {
                    day: "numeric",
                    month: "long",
                    year: "numeric"
                    })
                return (
                    <div>
                    <h1>Order-info</h1>
                    <div className="card card-account-info" style={styles}>
                        <ul>
                            <li>Order #{this.props.id}</li>
                            <li>Customer First Name: {this.props.customer_id.first_name}</li>
                            <li>Customer Last Name: {this.props.customer_id.last_name}</li>
                            <li>Customer Phone Number: {this.props.customer_id.phone_number}</li>
                            <li>The date of the order: {formattedDate}</li>
                        </ul>
                        <h3>The contents of the order:</h3>
                        <ol>
                            {orderItems}
                        </ol>
                    </div>
                    </div>
                    )
            }
}

let getOrder = async (id=id) => {
    let response = await fetch('http://flaviusbelisarius.pythonanywhere.com/api/orders/' + id)
    console.log(response)
    let data = await response.json()
    console.log('data1:', data)
    return data
}

let getOrdersByPhone = async (phoneNumber) => {
    let response = await fetch('http://flaviusbelisarius.pythonanywhere.com/api/orders/getByPhone/' + phoneNumber)
    console.log(response)
    let data = await response.json()
    console.log('data1:', data)
    return data
}


const orderInfo = function(id, needToActivateButtons) {
    getOrder(id).then(function(result) {
            if (result.served) {
                var activate = false;
            } else {
                activate = needToActivateButtons;
            }
            ReactDOM.render(<OrderItem
                            id={result.id}
                            date_ordered={result.date_ordered}
                            orderitem_set={result.orderitem_set}
                            customer_id={result.customer_id}
                            is_paid={result.is_paid}
                            />, document.getElementById('additional-info'))
            if (activate) {
                ReactDOM.render(<OrderManipulationButtons id={result.id} is_paid={result.is_paid} />,
                                document.getElementById('order-management-buttons'))
            } else {
                ReactDOM.render(<EmptyButtons />,
                                document.getElementById('order-management-buttons'))
            }
        })
}

const initOrderButtons = function(needToActivateButtons) {
    var orders = document.getElementsByClassName('order-button');
    console.log('orders:', orders)
    for (i = 0; i < orders.length; i++) {
        orders[i].addEventListener('click', function() {
            const id = this.id
            console.log(id)
            orderInfo(id, needToActivateButtons)
            })
    }
}


const initSearchInterface = function() {
    ReactDOM.render(<BonusesSearch />, document.getElementById('bonuses-search'))
}

const clearSearch = function() {
    ReactDOM.render(<EmptySearch />, document.getElementById('phone-order-list'))
}






