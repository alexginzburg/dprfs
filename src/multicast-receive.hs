import Network.Socket
import Network.Multicast

main = withSocketsDo $ do
	sock <- multicastReceiver "224.0.0.99" 9999
	let loop = do
		( msg, _, addr ) <- recvFrom sock 1024
		putStrLn ("from: " ++ show addr ++ " text = " ++ msg) 
		sendTo sock "Pong" addr
		loop in loop
