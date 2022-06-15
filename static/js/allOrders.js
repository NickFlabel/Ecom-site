
var getOrders = async () => {
    var response = await fetch('http://flaviusbelisarius.pythonanywhere.com/api/orders/all')
    let data = await response.json()
    console.log(data)
    return data
}

class SingleOrder extends React.Component {
    constructor(props) {
        super(props)
    }
    render () {
        let styles = {
                    width: "80%",
                    marginTop: "3px"
                }
        return(
            <li key={this.props.id}><button className={this.props.served ?
            "btn btn-sucsess order-button" : this.props.is_paid ?
            "btn btn-primary order-button" : "btn btn-warning order-button"}
            style={styles} id={this.props.id}>Order # {this.props.id}</button></li>
            )
    }
}

class AllOrders extends React.Component {
    constructor(props) {
        super(props)
    }
    render() {
        var allOrders = []
        for (let i = 0; i < this.props.orders.length; i++) {
            allOrders.push(<SingleOrder key={this.props.orders[i].id} id={this.props.orders[i].id} is_paid={this.props.orders[i].is_paid} served={this.props.orders[i].served} />)
        }
        return (
            <ol key="allOrders">
                {allOrders}
            </ol>
            )
    }
}

document.addEventListener('DOMContentLoaded', getOrders().then(result => {
    ReactDOM.render(<AllOrders
    orders={result}
    />, document.getElementById('all-orders-list'))
        }
    ).then(result => (initOrderButtons()
))
)


