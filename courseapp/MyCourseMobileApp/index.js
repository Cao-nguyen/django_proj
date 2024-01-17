import { registerRootComponent } from 'expo';
import App from './App';
import Home from './components/Home/Home';
import Test from './components/TestPackage/Test';

// registerRootComponent calls AppRegistry.registerComponent('main', () => App);
// It also ensures that whether you load the app in Expo Go or in a native build,
// AppRegistry.registerComponent('main', () => App)
// the environment is set up appropriately
registerRootComponent(App)