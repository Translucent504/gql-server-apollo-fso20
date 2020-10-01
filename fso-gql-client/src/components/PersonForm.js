import { useMutation } from '@apollo/client'
import React, { useState } from 'react'
import { ALL_PERSONS, CREATE_PERSON } from '../queries'



const PersonForm = ({ setError }) => {
  const [createPerson] = useMutation(CREATE_PERSON, {
    refetchQueries: [{ query: ALL_PERSONS }],
    onError: (error) => {
      setError(error.graphQLErrors[0].message)
    }
  })

  const [name, setName] = useState('')
  const [street, setStreet] = useState('')
  const [city, setCity] = useState('')
  const [phone, setPhone] = useState('')

  const handleSubmit = (e) => {
    e.preventDefault()
    createPerson({ variables: { name, street, city, phone } })

    setName('')
    setPhone('')
    setStreet('')
    setCity('')
  }


  return (
    <div>
      <h2>Create New</h2>
      <form onSubmit={handleSubmit}>
        <label htmlFor="name"> Name</label>
        <input value={name} onChange={({ target }) => setName(target.value)} id="name" type="text" />
        <label htmlFor="street"> street</label>
        <input value={street} onChange={({ target }) => setStreet(target.value)} id="street" type="text" />
        <label htmlFor="city">city </label>
        <input value={city} onChange={({ target }) => setCity(target.value)} type="text" id="city" />
        <label htmlFor="phone"> phone</label>
        <input value={phone} onChange={({ target }) => setPhone(target.value)} type="text" id="phone" />
        <button type="submit">Create</button>
      </form>

    </div>
  )
}

export default PersonForm
