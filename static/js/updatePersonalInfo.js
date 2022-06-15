var user = '{{ request.user }}'

function getToken(name) {
	   var cookieValue = null;
	   if (document.cookie && document.cookie !== '') {
	       var cookies = document.cookie.split(';');
	       for (var i = 0; i < cookies.length; i++) {
	           var cookie = cookies[i].trim();
	           if (cookie.substring(0, name.length + 1) === (name + '=')) {
	               cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
	               break;
	           }
	       }
	   }
    return cookieValue;
}

var csrftoken = getToken('csrftoken');


let getUser = async () => {
    var response = await fetch('http://flaviusbelisarius.pythonanywhere.com/api/getCurrentUser/')
    var data = await response.json()
    return data
}



let getPersonalInfo = async () => {
    var data = getUser().then(async function(result) {
        var response = await fetch('http://flaviusbelisarius.pythonanywhere.com/api/customer/' + result.id)
        var data = await response.json()
        console.log('data:', data)
        return data
    })
    return data
}



const initializing_button = document.getElementById('change-info-button');

initializing_button.addEventListener('click', function() {
    getPersonalInfo().then(function(result) {
    ReactDOM.render(<PersonalInfoForm
                    firstName={result.first_name}
                    lastName={result.last_name}
                    phoneNumber={result.phone_number}
                    username={result.user_id.username}
                    email={result.user_id.email}
                    />, document.getElementById('personal-info-list'))
})
})

class PersonalInfo extends React.Component {
        constructor(props) {
          super(props);
         }
        render() {
                return (
                    <ul key="personalInfo" className="list-group list-group-flush">
                        <li id="first-name" className="list-group-item">Your first name: {this.props.firstName}</li>
                        <li id="last-name" className="list-group-item">Your last name: {this.props.lastName}</li>
                        <li id="email" className="list-group-item">Your email: {this.props.email}</li>
                        <li id="phone-number" className="list-group-item">Your phone number: {this.props.phoneNumber}</li>
                    </ul>
                    )
            }
}

class PersonalInfoForm extends React.Component {
        constructor(props) {
          super(props);
          this.state = {
              firstName: this.props.firstName,
              lastName: this.props.lastName,
              email: this.props.email,
              phoneNumber: this.props.phoneNumber
          }
          this.handleChange = this.handleChange.bind(this);
          this.handleSubmit = this.handleSubmit.bind(this);
         }

        handleChange(event) {
            const target = event.target;
            const value = target.value;
            const name = target.name;
            this.setState({
                [name]: value
                })
            }

        handleSubmit(event) {
            event.preventDefault()
            var data = {
                phone_number: this.state.phoneNumber,
                first_name: this.state.firstName,
                last_name: this.state.lastName,
                email: this.state.email
            }
            console.log('There be window')
            const answer = window.confirm("Are you sure?")
            if (answer) {
            fetch('http://flaviusbelisarius.pythonanywhere.com/api/customer/update', {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken
                    },
                body: JSON.stringify(data)
            }).then(res => res.json).then(res => console.log(res)).then(getPersonalInfo().then(function(result) {
                                ReactDOM.render(<PersonalInfo
                                firstName={result.first_name}
                                lastName={result.last_name}
                                phoneNumber={result.phone_number}
                                username={result.user_id.username}
                                email={result.user_id.email}
                                />, document.getElementById('personal-info-list'))
                                }))
            }
        }

        render() {
                return (
                    <ul key="personalInfoForm" className="list-group list-group-flush">
                        <form onSubmit={this.handleSubmit}>
                        <li id="first-name" className="list-group-item">Your first name: <input name="firstName" type='text' value={this.state.firstName} onChange={this.handleChange} /></li>
                        <li id="last-name" className="list-group-item">Yout last name: <input name="lastName" type='text' value={this.state.lastName} onChange={this.handleChange} /></li>
                        <li id="email" className="list-group-item">Your email<input name="email" type='text' value={this.state.email} onChange={this.handleChange} /></li>
                        <li id="phone-number" className="list-group-item"><input name="phoneNumber" type='text' value={this.state.phoneNumber} onChange={this.handleChange} /></li>
                        <li id="phone-number" className="list-group-item"><input type='submit' value='Submit' /></li>
                        </form>
                    </ul>
                    )
            }
}


window.addEventListener('load', getPersonalInfo().then(function(result) {
                                ReactDOM.render(<PersonalInfo
                                firstName={result.first_name}
                                lastName={result.last_name}
                                phoneNumber={result.phone_number}
                                username={result.user_id.username}
                                email={result.user_id.email}
                                />, document.getElementById('personal-info-list'))
                                }
                                )
                                )





