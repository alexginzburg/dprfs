import Network.Socket
import Network.Multicast

main = withSocketsDo $ do
	( sock, addr ) <- multicastSender "224.0.0.99" 9999
	let loop = do
		sendTo sock "Ping" addr
		( msg, _, recv_addr ) <- recvFrom sock 1024
		putStrLn ("back from " ++ show recv_addr ++ " text " ++ msg)
		loop in loop
