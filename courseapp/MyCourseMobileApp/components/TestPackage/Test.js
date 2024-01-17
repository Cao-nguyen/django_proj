import { StyleSheet, Text, View } from "react-native"


const Test = () =>{
    return (
        <View style={style.boxCustom}>
            <View style={style2.boxCustom2}>
                <Text>
                    change text 2
                </Text>
            </View>
            <View style={style2.boxCustom2}>
                <Text>
                    change text 2
                </Text>
            </View>
        </View>
    )
}


const style = StyleSheet.create({
    boxCustom: {
        flex: 1
    }
})


const style2 = StyleSheet.create({
    boxCustom2: {
        flex: 2,
        backgroundColor: 'steelblue',
        justifyContent: "center", 
        alignItems: "center"
    }
})

export default Test