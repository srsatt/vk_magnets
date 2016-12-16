import React, {Component } from 'react'

class Person extends Component{
    handleClick(e){
      e.preventDefault();
      if (this.props.selected){
        this.props.deselectFriend(this.props.user_id)
      }
      else{
        this.props.selectFriend(this.props.user_id)
      }
    }
    render() {
        return (

            <div className={this.props.selected ? 'friend':'friend deselected'}>
              <a href="#" onClick={this.handleClick.bind(this)}  className='person'>
                <img className='avatar' src={this.props.avatar} />
              {/*<p className='name'> {this.props.first_name}</p>*/}
              </a>
            </div>
        );
    }
}

export default class Picker extends Component {
    componentDidMount(){
        //superagent
    }

    render() {
        const {friends,selected} = this.props
        var friend_list = friends.map(function(p, i){
            return <Person first_name={p.first_name} user_id={p.id} avatar={p.photo_max} selectFriend={this.props.selectFriend} deselectFriend={this.props.deselectFriend} key={i} selected={ selected.indexOf(p.id)>-1}/>
        }.bind(this));
        return (
              <div className='friend-names'>
                  {friend_list.length > 0 ? friend_list : <p>Список друзей пуст или что-то пошло не так.</p>}
              </div>
        );
    }
}
