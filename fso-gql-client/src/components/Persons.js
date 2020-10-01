import React, { useEffect, useState } from 'react'
import { useLazyQuery} from '@apollo/client'
import { FIND_PERSON } from '../queries'


const Persons = ({ persons }) => {
    const [getPerson, result] = useLazyQuery(FIND_PERSON)
    const [person, setPerson] = useState()
    const showPersonAdress = (name) => {
        getPerson({
            variables: {
                nameToSearch: name
            }
        })
    }
    useEffect(() => {
        if (result.data) {
            setPerson(result.data.findPerson)
        }
    }, [result])

    return (
        <table>
            <thead>
                <tr>
                    <th>Name</th>
                    <th>Phone</th>
                    <th>Address</th>
                </tr>
            </thead>
            <tbody>
                {persons.map(p => (
                    <tr key={p.name}>
                        <td>{p.name}</td>
                        <td>{p.phone}</td>
                        <td>{p.name === person?.name ? `${person.address.city}, ${person.address.street}` : <button onClick={() => showPersonAdress(p.name)}> Show Address</button>}</td>
                    </tr>))}
            </tbody>
        </table>
    )
}

export default Persons
