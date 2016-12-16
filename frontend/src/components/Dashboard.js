import React from 'react';
import request from 'superagent'
import FriendsSearch from '../components/FriendsSearch.js'
import DjangoCSRFToken from 'django-react-csrftoken'

// var agent = request(server);

class VkForm extends React.Component {
  constructor(props) {
    super(props);
    this.state = {value: ''};
    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }
  handleChange(event) {
    this.setState({value: event.target.value});

  }
  handleSubmit(event) {
    // alert('A name was submitted: ' + this.state.value);
    event.preventDefault();
    request.get('https://api.vk.com/method/users.get?user_ids='+this.state.value+'&v=5.25&fields=online,photo_50,bdate').end(function(err, res){
          var user_id = JSON.parse(res.text)['response'][0]['id']
          request.get('https://api.vk.com/method/friends.get?user_id='+user_id+'&v=5.25&fields=sex,photo_400_orig,photo_max,photo_max_orig').end(function(err, res){
                var friends = JSON.parse(res.text)['response']
                this.props.selectAll(friends['items'].map((p)=>{return p['id']}))
                this.props.setFriends(friends['items'].filter(function(person){
          if (person.photo_max.search(/(camera|deactivated)/)==-1) return true
          else return false;
          }
    ))

            }.bind(this));
      }.bind(this));

  }

  render() {

    return (
      <form onSubmit={this.handleSubmit}>
        <label>
          http://vk.com/
          <input type="text" value={this.state.value} onChange={this.handleChange} />
        </label>
        <input type="submit" value="Submit" />
      </form>
    );
  }
}


export default class Filter extends React.Component{
    constructor(props) {
      super(props);
    this.handleChange = this.handleChange.bind(this);
    }
      handleChange(event) {
        // console.log(event.target.value, event.target.checked)
        if (event.target.checked )
        {this.props.addTag(event.target.value);}
        else {this.props.removeTag(event.target.value)}
      }

      selectAllFriends(){
        this.props.selectAll(this.props.friends.map(function(p){return p['id']}))
      }
      sendFriendList(){
        // var cookie = 'csrftoken';
        // var header = 'X-CSRFToken';
        // var csrf = require('superagent-csrf-middleware')(cookie, header);
        // var csrf1 = csrf();
        // console.log(csrf1)
        var fr=this.props.friends.filter((p)=>{
          return (this.props.selected.indexOf(p.id)!=-1)
        })
        console.log(fr)
        request.post('/receivefriends')
        .send(this.props.friends.filter((p)=>{
          return (this.props.selected.indexOf(p.id)!=-1)
        })).end(()=>{})
      }
      //
      render() {
        const {friends,selected} = this.props

        if (friends.length <= 0 ){

          return (
            <div className='row'>
              <VkForm friends={friends.friends} selectAll={this.props.selectAll} setFriends={this.props.setFriends} />
            </div>
          );

        }
        else {
          return (<div className='row'>
            <button onClick={this.props.clearFriends}>Clear list</button>
            <button onClick={this.selectAllFriends.bind(this)}>Select All</button>
            <button onClick={this.props.deselectAll}>Deselect All</button>
            <button onClick={this.sendFriendList.bind(this)}>Send Friend List</button>
            <p>total friends selected: {this.props.selected.length}</p>
            <p>total lists: {Math.ceil(this.props.selected.length/54)}</p>
            <FriendsSearch friends={this.props.friends} selected={this.props.selected} setFriends={this.props.setFriends} selectFriend={this.props.selectFriend} deselectFriend={this.props.deselectFriend}/>

          </div>)
        }
      }
    }
