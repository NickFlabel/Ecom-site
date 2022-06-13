class BonusInfo extends React.Component {
        constructor(props) {
            super(props)
        }
        render () {
            const date = new Date(this.props.bonus.date_added)
            const formattedDate = date.toLocaleDateString("en-GB", {
                    day: "numeric",
                    month: "long",
                    year: "numeric"
                    })
            return(
            <li key={this.props.bonus.number_of_bonuses} >{this.props.bonus.number_of_bonuses} - {formattedDate}</li>
        )
        }
    }

    class Bonuses extends React.Component {
        constructor(props) {
          super(props);
         }
        render() {
                let bonuses = []
                for (let i = 0; i < this.props.bonuses_set.length; i++) {
                    bonuses.push(<BonusInfo key={i} bonus={this.props.bonuses_set[i]} />)
                }
                let styles = {
                    width: "75%",
                    height: "50vh",
                    overflowY: "scroll"
                }
                return (
                    <div>
                        <h1>Bonuses History</h1>
                        <div className="card card-account-info" style={styles}>
                            <ul>
                                {bonuses}
                            </ul>
                        </div>
                    </div>
                    )
            }
}

let getBonuses = async () => {
    let response = await fetch('http://flaviusbelisarius.pythonanywhere.com/api/bonuses/')
    let data = await response.json()
    console.log('data1:', data)
    return data
}

const bonuses = document.getElementById('bonuses-button');
bonuses.addEventListener('click', function() {
        getBonuses().then(function(result) {
        ReactDOM.render(<Bonuses
                        bonuses_set = {result.bonuses_set}
                        />, document.getElementById('additional-info'))
        })})