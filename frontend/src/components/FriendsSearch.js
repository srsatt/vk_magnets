import React, { Component } from 'react'

class SearchSuggestion extends React.Component {
  handleClick(e){

    if (this.props.selected.indexOf(this.props.person.text.id)>-1){
      this.props.deselectFriend(this.props.person.text.id)
      this.setState({text:'',results:[]})
    }
    else{
      this.props.selectFriend(this.props.person.text.id)
      this.setState({text:'',results:[]})
    }
    // e.preventDefault();
  }
render(){
  return (<a href="#" onClick={this.handleClick.bind(this)}>
    <div className={this.props.selected.indexOf(this.props.person.text.id)>-1 ? 'suggestion':'suggestion deselected'}>
      <img src={this.props.person.text.photo_max} />
      <p className='suggestion-name'>
        {this.props.person.text.first_name +" "+ this.props.person.text.last_name}</p>
    </div></a>);
}
}

class SearchResults extends React.Component {
  constructor(props) {
    super(props);
  }

  render() {

    var results_list = this.props.results.map(function(p, i){
        return <SearchSuggestion key={i} person={p} selectFriend={this.props.selectFriend} deselectFriend={this.props.deselectFriend} selected={this.props.selected} />
    }.bind(this));
    if(this.props.results.length == 0){
      return <div className='suggestions'></div>;
        }
    else{
    return <div className='suggestions'>{results_list}</div>;
        }
          }
  }
export default class FriendSearch extends React.Component {
  constructor(props) {
    super(props);
    this.state = {text:'',results:[]};
  }
  onChange (e) {
    // Don't give any result if string is empty
      this.setState({text:'',results:[]});
      if (e.target.value){
      this.setState({text:e.target.value, results: this.searchFriends(e.target.value,this.props.friends)})}
    }

    // this.setState({
    //   text: e.target.value,
    //   results: this.props.searchFriends(e.target.value)
    // });


  searchFriends (name,friends){
    return(
      friends
      .filter(function(n){

        // return n.first_name+' '+n.last_name.search(new RegExp(name, 'i')) !== -1;
        if ((n.first_name+' '+n.last_name).search(new RegExp(name, "i"))!==-1) return true
        else return false
      })
      .slice(0,10)
      .map(function(n){
        return {text: n};
      })
    );
  }

  render() {
    return (
      <div className='clean-search-container'>
        <input placeholder='Search...' autoComplete='off' className='clean-search-input' onBlur={()=>{setTimeout(()=>{this.setState({text:'',results:[]})}, 50);}} onChange={this.onChange.bind(this)} value={this.state.text}/>
        <SearchResults results={this.state.results} selectFriend={this.props.selectFriend} deselectFriend={this.props.deselectFriend} selected={this.props.selected}/>
      </div>
    );
  }
};
