

class CustomerBonuses extends React.Component {
    constructor(props) {
        super(props)
    }
    render () {
        return(
        <div>
            <p>{this.props.firstName} {this.props.lastName} ({this.props.username}) has {this.props.totalBonuses} bonuses</p>
        </div>
    )
    }
}
}

const getTotalBonuses = async function(phoneNumber) {
    var response = await fetch('http://flaviusbelisarius.pythonanywhere.com/api/customer/' + phoneNumber)
    if (response.ok) {
        var data = response.json()
        return data
    } else {
        alert('Invalid Phone Number')
    }
}


const initBonusesByPhoneNumberButton = function () {
    var button = document.getElementById('')
}