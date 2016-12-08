import React, { Component } from 'react'
import { bindActionCreators } from 'redux'
import { connect } from 'react-redux'
import Dashboard from '../components/Dashboard.js'
import Picker from '../components/Picker.js'
import * as friendsActions from '../actions/FriendsActions'
import * as selectedActions from '../actions/SelectedActions'

// import DjangoCSRFToken from 'django-react-csrftoken'
// <DjangoCSRFToken/>
// require("../styles/App.css")

class App extends Component {
  componentDidMount(){
      // var url = 'http://127.0.0.1:8000/team/filter';
      //superagent
  }
  render() {
    const { friends, selected} = this.props
    const { setFriends, clearFriends } = this.props.friendsActions
    const { selectFriend, deselectFriend, selectAll,deselectAll } = this.props.selectedActions
    return <div className='row'>
      <Dashboard friends={friends.friends} selected={selected.selected} setFriends={setFriends}  clearFriends={clearFriends} selectFriend={selectFriend} deselectFriend={deselectFriend} selectAll={selectAll} deselectAll={deselectAll}/>
      <Picker friends={friends.friends} selected={selected.selected} selectFriend={selectFriend} deselectFriend={deselectFriend} selectAll={selectAll} deselectAll={deselectAll}/>
    </div>
  }
}

function mapStateToProps(state) {
  return {
    selected: state.selected,
    friends: state.friends
  }
}

function mapDispatchToProps(dispatch) {
  return {
    selectedActions: bindActionCreators(selectedActions, dispatch),
    friendsActions: bindActionCreators(friendsActions, dispatch),

  }
}

export default connect(mapStateToProps, mapDispatchToProps)(App)
