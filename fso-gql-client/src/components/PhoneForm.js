import { useMutation } from '@apollo/client'
import React, { useEffect, useState } from 'react'
import { EDIT_NUMBER } from '../queries'



const PhoneForm = ({ setError }) => {
    const [changeNumber, result] = useMutation(EDIT_NUMBER)
    const [name, setName] = useState('')
    const [phone, setPhone] = useState('')

    const handleSubmit = (e) => {
        e.preventDefault()
        changeNumber({ variables: { name, phone } })
        setName('')
        setPhone('')
    }

    useEffect(() => {
        if (result.data && result.data.editNumber === null) {
            setError('Name not Found')
        }
    }, [result.data]) //eslint-disable-line

    return (
        <form onSubmit={handleSubmit}>
            <label htmlFor="name">Name</label>
            <input onChange={({ target }) => setName(target.value)} value={name} id='name' type="text" />
            <label htmlFor="phone">Phone</label>
            <input onChange={({ target }) => setPhone(target.value)} value={phone} id='phone' type="text" />
            <button type='submit'>Change</button>
        </form>
    )
}

export default PhoneForm
