console.log('reactOrders is loaded')


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

const initOrderButtons = function() {
    var orders = document.getElementsByClassName('order-button');
    console.log('orders:', orders)
    for (i = 0; i < orders.length; i++) {
        orders[i].addEventListener('click', function() {
            const id = this.id
            console.log(id)
            getOrder(id).then(function(result) {
            ReactDOM.render(<OrderItem
                            id={result.id}
                            date_ordered={result.date_ordered}
                            orderitem_set={result.orderitem_set}
                            customer_id={result.customer_id}
                            />, document.getElementById('additional-info'))
        })})
    }
}