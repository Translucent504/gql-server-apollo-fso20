import React, { useState } from 'react';
import './App.css';
import { useQuery } from '@apollo/client'
import Persons from './components/Persons';
import PersonForm from './components/PersonForm';
import { ALL_PERSONS } from './queries';
import PhoneForm from './components/PhoneForm';

const Notification = ({message}) => {
  return (
    <h1 style={{color:'red'}}>{message}</h1>
  )
}



function App() {
  const [errorMsg, setErrorMsg] = useState(null)

  const result = useQuery(ALL_PERSONS)
  if (result.loading) {
    return <h1>LOADING...</h1>
  }

  const notify = (msg) => {
    setErrorMsg(msg)
    setTimeout(() => {
      setErrorMsg(null)
    }, 3000)
  }
  
  return (
    <div className="App">
      {errorMsg && <Notification message={errorMsg}/>}
      <PhoneForm setError={notify}/>
      <PersonForm setError={notify}/>
      <Persons persons={result.data.allPersons}/>
    </div>
  );
}

export default App;
