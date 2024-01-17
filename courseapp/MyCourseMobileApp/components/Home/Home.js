import { ActivityIndicator, Text, TextInput, View } from 'react-native';
import hStyle from './hStyle';
import myStyle from '../../Styles/myStyle';
import React, { useEffect } from 'react';
import api, {endpoints} from '../../configs/api';


const Home = () =>{
    const [courses, setCourses] = React.useState(null)

    useEffect(()=>{
        const loadCourses = async () => {
            try{
                let res = await api.get(endpoints['courses'])
                setCourses(res.data.results)
            }
            catch(ex){
                console.error(ex);
            }
        }

        loadCourses()
    }, [])
    return (
        <View style={myStyle.container}> 
            <Text style={hStyle.subject}>
            Home
            </Text>
            {courses === null ? <ActivityIndicator/>: <>
                {
                    courses.map( c => (
                        <Text key={c.id}>
                            {c.subject}
                        </Text>
                    ))
                }
            </>}
        </View>
    )
}


export default Home